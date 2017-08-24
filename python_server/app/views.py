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


FB_APP_ID = '1462100957178030'
FB_APP_SECRET = '52dcf535d81d792d4da51eeac3f11fb3'

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
                                 'access_token'], version='2.8')
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
            return render_template('index.html', app_name=session.get('page_name'), user=g.user, recent_posts=recent_posts)
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


@app.route('/posts/<post_type>', methods=['POST'])
def handle_submissions(post_type=None):
    """
        Handles the submissions of the quick-posting.
    """
    print("handling submission: " + str(post_type))
    if(post_type == None):
        return render_template('submit-status.html', data={"message": "Error"})
    else:
        try:
            page_graph = get_page_graph(GraphAPI(access_token=g.user['access_token'], version='2.8'))    
            if (post_type == "quick-post"):
                publish_at = None
                publish= True
                if(request.form.get('datetime') != ''):
                    jt = request.form.get('datetime').split(' ')
                    daily = jt[1].split(':')
                    publish_at = int(time.mktime(datetime.datetime.strptime(jt[0], "%Y-%m-%d").timetuple()) + int(daily[0]) * 60 * 60 + int(daily[1]) * 60)
                    publish = False
                if(len(request.files['picture'].filename) > 0):
                    # has a picture
                    print("posting an image")
                    status = page_graph.put_photo(parent_object=session.get('page_access_token'), image=request.files.get("picture"), message=request.form["message"], scheduled_publish_time=publish_at, published=publish)
                else:
                    # no picture
                    print("posting a status")
                    status = page_graph.put_object(parent_object=session.get('page_access_token'),connection_name="feed",message=request.form["message"], scheduled_publish_time=publish_at, published=publish)
                date = time.strftime('%l:%M%p')
                return render_template('submit-status.html', data={"message": "Submitted at: " + date})
            elif (post_type == "get_comments"):
                print("getting comments")
                # pdb.set_trace()
                post_id = request.args.get('id')
                if(post_id != None):
                    comments = page_graph.get_connections(id=post_id, connection_name='comments')['data']
                    if(comments != None):
                        return render_template('comments.html', comments=comments, post_id=post_id)
                    # pdb.set_trace()
        except Exception as e:
                print("ERROR: " + str(e))
                return render_template('submit-status.html', data={"message":str(e)})
    return render_template('submit-status.html', data={"message":"Error"})


def get_page_graph(graph):
    # Get page token to post as the page. You can skip 
    # the following if you want to post as yourself. 
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == session.get('page_access_token'):
            page_access_token = page['access_token']
            session['page_name'] = page.get('name')
            graph = GraphAPI(access_token=page_access_token, version='2.8')
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
            graph = GraphAPI(result['access_token'], version='2.8')
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
