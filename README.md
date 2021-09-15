# ExecBJJ Website
![image](https://user-images.githubusercontent.com/42610577/133406469-cfa248d1-02d7-4d19-b337-c19859cc5578.png)
[Live Deployed Website](https://stark-earth-52954.herokuapp.com/)



## Author
Sam Mc Nally


## Project Overview
This site is design with a landing page for lead capturing as well as a user message board for authenticated users. Users can create an account, login, post messages on the message board, edit and delete this messages as well as being able to sign up for newsletter updates and sumbit queries through a contact form. 

## HOW TO USE
To use this website the steps are as follows.

- Step 1: Login, if user does not have an account they can login by clicking the "Click here to register" link on the login form.
![image](https://user-images.githubusercontent.com/42610577/133413663-9bf0bf65-2737-40b0-941c-51a9026b6b35.png)
- Step 2: Once logged in a user will be redirected to the dashboard, a success message will flash to say that they have logged in.
![image](https://user-images.githubusercontent.com/42610577/133413946-2b3e6f16-88ca-4990-b2a1-05218e03000c.png)
- Step 3: Users can create posts by filling this the create post form. Each post object has the property of "Owner" set to the user by default to allow for permission controls so that only the owner of a post can edit of delete it.
![image](https://user-images.githubusercontent.com/42610577/133414066-3b644c07-dad5-491e-a08a-25c5e9965430.png)
- Step 4: Users can edit or delete their posts by clicking on the edit or delete buttons that show up on the posts they own. All of a users posts are shown in the "My Posts" section if they scroll down past the message form.
![image](https://user-images.githubusercontent.com/42610577/133414333-26fce672-0e6d-4970-97c6-61a8ed878a46.png)

### Unauthenticated User
Unauthenticated Users can access the landing page, login page and registration page. The site is built with access controls to stop unauthenticated users from accessing the dashboard as well as posting, post editing and post deleting functionality.
- A login Flask decorator is used to check that if the session object does not contain the property of logged in, the user will be redirected to a login page.

``` def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("You must be logged in to access", "bg-red-400")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
```

### Standard User
- A standard user can make posts to the message board. By default, each post object has the property of "Owner" set to the user by default to allow for permission controls so that only the owner of a post can edit of delete it.

When a new user is created the user property in the session object is assigned as the value of "Owner.

``` class Post:
    def create(self, form):
        post = {
        "_id": uuid.uuid4().hex,
        "owner": session['user'],
        "date": datetime.now(),
        "post": form.post.data
        }

        db.posts.insert_one(post)
        return True
```
        
Permission controls at the route level are then implemented to limit editing and deleting to that of the post owner.

``` @app.route('/posts/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = PostForm(request.form)
    post = db.posts.find_one({"_id": id})
    if session['user']['_id'] == post['owner']['_id']:
        form.post.data = post['post']
        if request.method == "POST" and form.validate():
            post = Post()
            new_form = PostForm(request.form)
            post.edit(id, new_form)
            flash("Post has been updated", "bg-yellow-400")
            return redirect(url_for('dashboard'))
        return render_template("edit_post.html", form=form)
    flash("Permission denied, you must be the owner of this post to edit", "bg-yellow-400")
    return redirect(url_for('dashboard'))
```

### Admin User
- Currently there is no permission restricted only to admin users via the interface of the website.

# Table of Contents
Copy your readme to http://ecotrust-canada.github.io/markdown-toc/ to make a table of contents.  This will help assessors to see the structure of your readme. Just test it out ast this tool isn't perfect. It tends to mess up with special characters like dashes.

## UX
As this is a CRUD based application the key UX features for this site are clear and defined input for accessability. Examples of this can be seen on the edit and delete buttons for posts.\
![image](https://user-images.githubusercontent.com/42610577/133416933-fef1c338-7447-4de6-8aa0-adac275e7bd1.png)

### Strategy
The strategy behind this website is to use of for a company that I own that is in the process of opening back up after being shut for over a year.

### Project Goals
The goal of this project is to deliver a simple, user friendly and intuitive application that allows user to create, read, update and delete message postings limited to 180 characters.

#### User Goals
As a user I want to have a clear and intuitive experience through out the application with consisten visual feedback in the form of flashed messages as I interact with the website.

#### Developer Goals
As a developer I aim to produce an CRUD application with User Authentication as well as a defensive programming design strategy to ensure that user's data is protected.

#### Website Owner Goals
As a product owner I aim to have a piece of software that is built with clean foundational architecture that provides for the ability to add more directly monetisable features like premium membership content a payment integrations into the site in the near future.


### User Stories
As a User I want to be able to sign up to a newsletter, submit queries via a contact form, create an account, login, make posts, edit posts, delete posts.


### Design Choices
The most prominent design choices in this application are to be found in the visual feedback of the alert messages with Green being used for success messages, Yellow for standard operations like post editing and Red for error messages.

As well as this providing users with their own data aggregated into the "My Posts" section is design to that users can access their posts directly from the message board and have the posts that they own filtered in the "My Posts" section.

#### Colors
The colours used in this project are simple Greys and Black for structual elements of the pages, Red and Blue for the edit and delete button and Green, Yellow and Red for visual feedback in the alert messages depening on the nature of the interaction.

#### Typography
The typography used is Helvetica. I initially wanted to use Montserrat but I found that Helvetica translated across devices better than Montserrat.

#### Images
The images used are all relating to the activities of the company. They are mostly high quality JPEGs.

#### Design Elements

Forms.\
![image](https://user-images.githubusercontent.com/42610577/133421600-c847bf60-a61a-4e50-9efe-48909b2d5563.png)

Input Buttons.\
![image](https://user-images.githubusercontent.com/42610577/133421767-1c1e08df-602c-4b66-aec0-11bc2ef7ef14.png)
![image](https://user-images.githubusercontent.com/42610577/133416933-fef1c338-7447-4de6-8aa0-adac275e7bd1.png)

Cards.\
![image](https://user-images.githubusercontent.com/42610577/133421909-4859cdd9-ab79-4dda-ba73-dcc03479b64f.png)


#### Animations and Transitions

- discuss any special animations or transitions you've programmed 
- special hover state effects


#### Custom Javascript
There is a timeout function on the alert messages so that the dissapear after 5 seconds.
``` <script>
  window.setTimeout(
    "document.getElementById('alert').style.display='none';",
    5000
  );
</script>
 ```

### Wireframes

I built full mobile and desktop mockups using Adobe XD.\
![image](https://user-images.githubusercontent.com/42610577/133422184-ef3cb867-7ee6-4a68-8f64-f924d112ab0e.png)


### Features
Lead capture form.\
![image](https://user-images.githubusercontent.com/42610577/133422290-92cba907-24b7-4200-9edd-c9c18f378f0d.png)

Contact form.\
![image](https://user-images.githubusercontent.com/42610577/133422362-b50e0daa-b446-4a27-8de2-2aed01a22fe3.png)

Login page.\
![image](https://user-images.githubusercontent.com/42610577/133422473-d04628b3-b5da-4d6d-8f0c-4e6f5d384c04.png)

Registration page.\
![image](https://user-images.githubusercontent.com/42610577/133422519-a8c4ce11-0085-4230-8c24-cd24d763f13f.png)

Dashboard with post form.\
![image](https://user-images.githubusercontent.com/42610577/133422600-286dce18-91b8-41f4-a483-03100506b733.png)

User's posts section.\
![image](https://user-images.githubusercontent.com/42610577/133422675-2dab0d0a-0a1a-4cc4-899b-41e921e93694.png)


#### Implemented Features

For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

It's easiest to break this section down into by pages and common page components such as home page, products page, product detail page, product sort buttons, navigation, and footer. Call out differences between viewports as needed. 

Don't forget your 404 and 500 error pages.

#### Future Features

Use this section to discuss plans for additional features to be implemented in the future:

If you end up not developing some features you hoped to implement, you can include those in this section.


# Information Architecture

As part of the requirements for this project you need to have at least 2 original data models.  It's this section that discusses your data and how each piece relates to another.

 - [draw.io](https://about.draw.io/features/) - is a free program that can be used to create Entity Relationship diagrams and CRUD flow diagrams.

## Entity Relationship Diagram

Use some type of spreadsheet or even draw out one by hand, but you should show how your data models are related to each other  or what those tables are even if they are entirely separate from each other. 

## CRUD Flow Diagrams

It might be overkill, but you could document the flow of how your CRUD operation logic works if its full of complex logic. Using a flow diagram or process diagram might make it easier for accessors to understand the inner workings of your program.


## Database Choice
Write out which database(s) you used and why sometimes you use a different one for local vs production.

### Data Models
Show the accessors you know your data. If you end up using some data models from an example project, call that out and don't be as detailed about writing those up unless you added to them.  

Each data model that you created yourself should have its Fields, Field Type and any validation documented.  You should also cross-reference any code in your repository that relate to CREATE, READ, UPDATE, DELETE operations for these models. 


# Technologies Used

In this section, you should mention the languages, frameworks, libraries, databases and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- If you included a js file that isn't your own, add it here.

- If you included a css file that isn't your own, add it here.

- Common 3rd party technologies to list:
  - wirefames
  - favicons
  - color palette images
  - fonts
  - CSS Frameworks
  - markdown tables
  - markdown table of contents
  
Please note, if this gets more than 5 items, you may want to break it down into logical subsections

## Programming Languages

- [CSS3](https://www.w3schools.com/w3css/default.asp) - used to style DOM appearance. 
- [HTML5](https://www.w3schools.com/html/default.asp) -  used to define DOM elements. 
- [JQuery](https://jquery.com) - used to initialize handlers for user interactive elements such as Bootstrap framework pieces like: check boxes, date pickers, menu toggles.
- [JavaScript](https://www.javascript.com/)  -  used to help handle challenge member entry.
- [Python](https://www.python.org/) the project back-end functions are written using Python. Django and Python is used to build route functions.
- [Flask](https://flask-doc.readthedocs.io/en/latest/) - python based templating language
- [mongodb](https://www.mongodb.com/cloud/atlas)- a fully-managed cloud database used to store manage and query data sets
- [Markdown](https://www.markdownguide.org/) Documentation within the readme was generated using markdown

[Back To Table of Contents](#table-of-contents)

## Framework & Extensions
- list out references to all the JS, CSS and requirement packages you used in your project. Include a short reason why this technology was important to your project.


## Fonts

Provide a link to any google or other fonts used on your site using markdown links:

- Base Font: [Orbitron](https://fonts.google.com/?query=orbitron&selection.family=Orbitron) 
- Header Font: [Exo](https://fonts.google.com/?query=orbitron&selection.family=Exo) 
- Button Icons: [Font Awesome 5](https://fontawesome.com/icons?d=gallery)

## Tools
In this section you should reference any 3rd party tools you used to make your project or readme. Wireframes, faviocon, github, color palette generators, heroku and any testing emulators are things that belong in this section.
[Back To Table of Contents](#table-of-contents)

## APIs

List out the API's  you used for this project. 

# Defensive Programming

Sites with admin rules and roles opens a site up to hacking especially if your users are savvy and notice url parameters correlate to database object manipulation.  If you did anything above the basics to defend your application against hacking write them out here.
   
[Back To Table of Contents](#table-of-contents)

## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

### Validation Testing
You should try to ensure you code is valid and follows proper indentation.  In this section you should write up any websites you used to validate your code. As your projects becomes more complex these tools may change.

- [CSS Validator](https://jigsaw.w3.org/css-validator/) Note, any error associated with root: color variables were ignored.
- [HTML Validator](https://validator.w3.org/)

### Cross Browser and Cross Device Testing
Create a table that lists out what devices, browsers, and operating system you tested your application on and a brief description of why you chose the mixture you did. The point is to prove that you looked at the site across various browsers, operating systems, and viewport breakpoints.

| TOOL / Device                 | BROWSER     | OS         | SCREEN WIDTH  |
|-------------------------------|-------------|------------|---------------|
| real phone: motog6            | chrome      | android    | XS 360 x 640  |
| browser stack: iPhone5s       | safari      | iOs        | XS 320 x 568  |
| dev tools emulator: pixel 2   | firefox     | android    | SM 411 x 731  |
| browserstack: iPhone 10x      | Chrome      | iOs        | SM 375 x 812  |
| browserstack: nexus 7 - vert  | Chrome      | android    | M 600 x 960   |
| real tablet: ipad mini - vert | safari      | iOs        | M 768 x 1024  |
| browserstack: nexus 7 - horiz | firefox     | android    | LG 960 x 600  |
| chrome emulator: ipad - horiz | safari      | iOs        | LG 1024 x 768 |
| browserstack                  | Chrome      | windows    | XL 1920 x 946 |
| real computer: mac book pro   | safari 12.1 | Mohave     | XL 1400 x 766 |
| browserstack                  | IE Edge 88  | windows 10 | XL 1920 x 964 |

### Automated Testing
Whenever it is feasible, automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

If you did not run automating testing. State why you chose not to.

### Manual Testing

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.
    
Here is a [Manual Testing Template](https://docs.google.com/spreadsheets/d/189VpSeEG9oevSRhvb2WZl8zCk9L3s2iWQyrJ_1jjAGQ/edit?usp=sharing) that you can use as a starting point to keep track of your testing efforts. Make a copy of it in your own account and update as needed to reflect the browsers you are testing and features.  

It's ok to spot check specific functionality across devices and browsers but each page should be viewed as a whole for each device/browser combo at least once.

A quick way to check if items are exceeding the screen width of a project is to run this javascript in the console for various screen emulations:

```
var docWidth = document.documentElement.offsetWidth;
[].forEach.call(document.querySelectorAll('*'),function(el){if(el.offsetWidth > docWidth){console.log(el);}});
```

### Defect Tracking

You should mention  any  bugs or problems you discovered during your testing, even if you haven't addressed them yet.

Here is a [Defect Tracking Template](https://docs.google.com/spreadsheets/d/1tYB4X4wTCNEW_Y1no3hsGbclh2bLokl_I5Ev3s5EuJA/edit?usp=sharing) you use as a starting point to track defects. Make a copy of the sheet to your own account and update the Features sheet to match your project. 


### Defects of Note
Some defects are more pesky than others. Highlight 3-5 of the bugs that drove you the most nuts and how you finally ended up resolving them.


### Outstanding Defects
It's ok to not resolve all the defects you found. If you know of something that isn't quite right, list it out and explain why you chose not to resolve it.

### Validation

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages).

In particular, you should provide all details of the differences between the deployed version, and the development version, if any.

Remember to use proper markdown for commands and enumerated steps.

### Deploy Locally

Write out the steps you take starting from cloning the repository in github or clicking a gitpod button to run your code locally. Test it out and make sure it works. This can be running from your IDE of choice like VSCode or PyCharm or GitPod.

You may want to re-watch the videos when writing up this section.

### Deploy To Heroku

Write out steps you would take and test them to deploy your code to Heroku. Include a table of configuration variables as needed in your settings.py file without exposing your own values. Include links to users on how to set up such accounts for AWS, STRIPE or other programs.  

You may want to re-watch the videos when writing up this section.

## Credits

To avoid plagiarism amd copyright infringement, you should mention any other projects, stackoverflow, videos, blogs, etc that you used to gather imagery or ideas for your code even if you used it as a starting point and modified things. Giving credit to other people's efforts and ideas that saved you time acknowledges the hard work others did. 

### Content

Use bullet points to list out sites you copied text from and cross-reference where those show up on your site

### Media

Make a list of sites you used images from. If you used several sites try to match up each image to the correct site. This includes attribution for icons if they came from font awesome or other sites, give them credit.

### Acknowledgments

This is the section where you refer to code examples, mentors, blogs, stack overflow answers and videos that helped you accomplish your end project. Even if it's an idea that you updated you should note the site and why it was important to your completed project.

If you used a CodeInstitute Example project as a starting point. Make note of that here.
