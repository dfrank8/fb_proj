from facebook import get_user_from_cookie, GraphAPI
from flask import g, jsonify, render_template, redirect, request, session, url_for
from flask_compress import Compress
from flask_assets import Environment, Bundle
from app import app, db
from models import User
import pdb
import sys
import time
import datetime
from dynamo_helper import Dynamo_Wrapper


FB_APP_ID = '1462100957178030'
FB_APP_SECRET = '52dcf535d81d792d4da51eeac3f11fb3'

dynamo_drafts = Dynamo_Wrapper(table_name ='drafts', primary_key = 'app_id')

Compress(app)
assets = Environment(app)

js_bundle = Bundle(
    'js/copytoclipboard.js',
    'js/script.js',
    filters='jsmin', output='gen/jsmin.js')

css_bundle = Bundle(
    'css/bootstrap.min.css',
    'css/font-awesome.min.css',
    'css/animate.min.css',
    'css/style.css',
    'css/colors/treehoppr.css',
    filters='cssmin', output='gen/cssmin.css')

assets.register('js_all', js_bundle)
assets.register('css_all', css_bundle)
# Facebook app details


@app.route('/', methods=['GET', 'POST'])
@app.route('/<number_of_posts>', methods=['GET'])
def index(number_of_posts=5):
    """
    Index is used for the primary login and single-page interactivity.
    See the switches below.
    """
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    if request.method == 'POST':
        if g.user:
            # this means the app-choosing is happening.
            if(len(request.form) > 0):
                page_id = request.form.get('page-id')
                # set the token and wait for the re-route
                session['page_access_token'] = page_id
                return jsonify({'success': True})
        return jsonify({'success': False})
    else:
        print("not post")
        if g.user:
            print("have user")
            gen_graph = GraphAPI(access_token=g.user[
                                 'access_token'], version='2.9')
            if('page_access_token' not in session.keys()):
                # Serve this page for the user to select what page they want to
                # interact with.
                resp = gen_graph.get_object('me/accounts')
                page_options = []
                for owned_page in resp['data']:
                    page_options.append({
                        'name': owned_page['name'],
                        'id': owned_page['id']
                     })
                return render_template('choose_page.html', app_id=FB_APP_ID, app_name=session.get('page_name'), user=g.user, page_options=page_options)
            page_graph = get_page_graph(gen_graph)
            # BUILD MAIN INDEX
            # Recent posts
            recent_posts = []
            unpublished_posts = []
            posts = page_graph.get_connections(session.get(
                'page_access_token'), 'posts', limit=number_of_posts)
            for post in posts.get('data'):
                try:
                    recent_posts.append({
                    'id': post['id'],
                    'message': post['message'],
                    'message_trim': post['message'][0:25],
                    'like_count': len(page_graph.get_connections(id=post['id'], connection_name='likes')['data']),
                    'comment_count': len(page_graph.get_connections(id=post['id'], connection_name='comments')['data'])
                })
                except:
                    continue
            response = dynamo_drafts.query(FB_APP_ID)
            drafts = []
            if(len(response.get('Items')) > 0):
                for draft_id in response.get('Items')[0].get('drafts'):
                    draft = page_graph.get_object(str(draft_id))
                    drafts.append(
                        {
                            'id' : str(draft.get('id')),
                            'message' : str(draft.get('message')),
                            'created_time' : str(draft.get('created_time'))
                        })
            kwargs = {}
            if(len(drafts) > 0):
                kwargs['drafts'] = drafts
            if(len(recent_posts) > 0):
                kwargs['recent_posts'] = recent_posts
            return render_template('index.html', app_name=session.get('page_name'), user=g.user, **kwargs)
    # Otherwise, a user is not logged in.
    print("going to the login page")
    return render_template('login.html', user=g.user)


@app.route('/logout')
def logout():
    """Log out the user from the application.

    Log out the user from the application by removing them from the
    session.  Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    print("logout")
    g.user = None
    session.pop('page_access_token', None)
    session.pop('user', None)
    return redirect(url_for('index'))


def fb_put_object(page_graph, parent_object, is_image, **kwargs):
    # pdb.set_trace()
    api_call = None
    if(is_image):
        pass
        api_call = page_graph.put_photo
    else:
        # not image
        pass
        api_call = page_graph.put_object
    return api_call(parent_object=parent_object, **kwargs)

    # status = page_graph.put_photo(parent_object=session.get('page_access_token'), image=request.files.get("picture"), message=request.form["message"], scheduled_publish_time=publish_at, published=publish)
    # status = page_graph.put_object(parent_object=session.get('page_access_token'),connection_name="feed",message=request.form["message"], scheduled_publish_time=publish_at, published=publish)

def parse_date_time(jt):
    jt = jt.split(' ')
    daily = jt[1].split(':')
    return int(time.mktime(datetime.datetime.strptime(jt[0], "%d/%m/%Y").timetuple()) + int(daily[0]) * 60 * 60 + int(daily[1]) * 60)

@app.route('/posts/<post_type>', methods=['POST'])
def handle_submissions(post_type=None):
    """
        Handles the submissions of the quick-posting.
    """
    delete_draft("123")
    print("handling submission: " + str(post_type))
    if(post_type == None):
        return render_template('submit-status.html', data={"message": "Error"})
    else:
        try:
            is_draft = False
            args = {}
            page_graph = get_page_graph(GraphAPI(access_token=g.user['access_token'], version='2.9'))    
            if (post_type == "quick-post"):
                # build the args for quick-post
                publish_at = None
                if( request.form.get('is_draft') == None ):                    
                    if(request.form.get('datetime') != ''):
                        args['publish_at'] = parse_date_time(request.form.get('datetime'))
                        args['published'] = False
                    else:
                        args['published'] = True
                else:
                    #I have a draft
                    args['published'] = False

                is_image = False
                args['message'] = request.form["message"]
                if(len(request.files['picture'].filename) > 0):
                    # has a picture
                    print("posting an image")
                    args['image'] = request.files.get("picture")
                    is_image = True
                else:
                    args['connection_name'] = "feed"
                
                status = fb_put_object(page_graph,session.get('page_access_token'),is_image,**args)
                if not args['published'] and 'id' in status.keys():
                    # it's a draft, let's break out and do draft stuff. 
                    handle_draft_submission(str(status.get('id')))
                date = time.strftime('%l:%M%p')
                return render_template('submit-status.html', data={"message": "Submitted at: " + date})
            elif (post_type == "get_comments"):
                print("getting comments")
                post_id = request.args.get('id')
                if(post_id != None):
                    comments = page_graph.get_connections(id=post_id, connection_name='comments')['data']
                    if(comments != None):
                        return render_template('comments.html', comments=comments, post_id=post_id)
        except Exception as e:
                print("ERROR: " + str(e))
                return render_template('submit-status.html', data={"message":str(e)})
    return render_template('submit-status.html', data={"message":"Error"})

def handle_draft_submission(post_id):
    # pdb.set_trace()
    response = dynamo_drafts.query(FB_APP_ID)
    if(len(response.get('Items')) > 0):
        # we have a array already! we need to update it
        dynamo_drafts.update_post_list(FB_APP_ID,post_id)
    else:
        item = {
            'app_id' : FB_APP_ID,
            'drafts' : [post_id]
        }     
        status = dynamo_drafts.addItem(item)
    pdb.set_trace()

def delete_draft(post_index):
    dynamo_drafts.delete_draft(FB_APP_ID, post_index)
    pdb.set_trace()


def get_page_graph(graph):
    # Get page token to post as the page. You can skip 
    # the following if you want to post as yourself. 
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == session.get('page_access_token'):
            page_access_token = page['access_token']
            session['page_name'] = page.get('name')
            graph = GraphAPI(access_token=page_access_token, version='2.9')
            return graph

@app.before_request
def get_current_user():
    """Set g.user to the currently logged in user.

    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.  A currently logged in user is
    determined by seeing if it exists in Flask's session dictionary.

    If it is the first time the user is logging into this application it will
    create the user and insert it into the database.  If the user is not logged
    in, None will be set to g.user.
    """

    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    # pdb.set_trace()
    if session.get('user'):
        g.user = session.get('user')
        return
    # pdb.set_trace()  
    if(request.cookies  == {}):
        print("no cookies")
    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)
    # pdb.set_trace()
    # If there is no result, we assume the user is not logged in.
    if result:
        # Check to see if this user is already in our database.
        user = User.query.filter(User.id == result['uid']).first()

        if not user:
            # Not an existing user so get info
            graph = GraphAPI(result['access_token'], version='2.9')
            profile = graph.get_object('me')
            if 'link' not in profile:
                profile['link'] = ""

            # Create the user and insert it into the database
            user = User(id=str(profile['id']), name=profile['name'],
                        profile_url=profile['link'],
                        access_token=result['access_token'])
            db.session.add(user)
        elif user.access_token != result['access_token']:
            # If an existing user, update the access token
            user.access_token = result['access_token']

        # Add the user to the current session
        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token)

    # Commit changes to the database and set the user as a global g.user
    db.session.commit()
    g.user = session.get('user', None)
