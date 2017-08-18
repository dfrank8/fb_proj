from facebook import get_user_from_cookie, GraphAPI
from flask import g, jsonify, render_template, redirect, request, session, url_for
from flask_compress import Compress
from flask_assets import Environment, Bundle
from app import app, db
from models import User
import pdb


FB_APP_ID = '1462100957178030'
FB_APP_NAME = 'Interview_Proj'
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

@app.route('/', methods=['GET','POST'])
def index():
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    if request.method == 'POST':
        if g.user:  
            # this means the app-choosing is happening.
            if(len(request.form)>0):
                page_id = request.form.get('page-id')
                # session['page_graph'] = get_page_graph(GraphAPI(access_token=g.user['access_token'], version='2.9'))
                # set the token and wait for the re-route
                session['page_access_token'] = page_id
                return jsonify({'success':True})
        return jsonify({'success': False})
    else:
        print("not post")
        if g.user:
            print("have user")
            gen_graph = GraphAPI(access_token=g.user['access_token'], version='2.9')
            if('page_access_token' not in session.keys()):
                # Serve this page for the user to select what page they want to interact with.
                resp = gen_graph.get_object('me/accounts')
                page_options = []
                for owned_page in resp['data']:
                    page_options.append({
                        'name':owned_page['name'],
                        'id':owned_page['id']
                     })
                return render_template('choose_page.html', app_id=FB_APP_ID, app_name=FB_APP_NAME, user=g.user, page_options=page_options)
            
            # status = page_accessor.put_object(parent_object="1801207079907523",connection_name="feed",message=msg)
            return render_template('index.html', app_id=FB_APP_ID, app_name=FB_APP_NAME, user=g.user)
    # Otherwise, a user is not logged in.
    print("going to the login page")
    return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME, user=g.user)

@app.route('/logout')
def logout():
    """Log out the user from the application.

    Log out the user from the application by removing them from the
    session.  Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    print("logout")
    g.user = None
    session.pop('page_access_token',None)
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/posts/<post_type>', methods=['POST'])
def handle_submissions(post_type = None):
    if(post_type == None):
        return jsonify({'success': False})
    elif (post_type == "quick-post"):
        # pdb.set_trace()
        page_graph = get_page_graph(GraphAPI(access_token=g.user['access_token'], version='2.9'))
        status = page_graph.put_object(parent_object=session.get('page_access_token'),connection_name="feed",message=request.form["message"])
        # pdb.set_trace()


def get_page_graph(graph):
    # Get page token to post as the page. You can skip 
    # the following if you want to post as yourself. 
    resp = graph.get_object('me/accounts')
    page_access_token = None
    # pdb.set_trace()
    for page in resp['data']:
        if page['id'] == session.get('page_access_token'):
            page_access_token = page['access_token']
            graph = GraphAPI(page_access_token)
            return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

# @app.route('/peak')
# def peak():
#     return render_template

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
            graph = GraphAPI(result['access_token'])
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
