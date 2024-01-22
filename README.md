# LYNCSYNC
#### Video Demo:  <https://youtu.be/yLb8nTLpbAM>
#### Description:

LYNCSYNC – Your Links, Your Freedom, Your Devices

LYNCSYNC is a web application developed to address the common challenge of seamlessly syncing links across various devices, including smart TVs. The primary objective is to provide users with a convenient and secure platform for managing and accessing links effortlessly. The application allows users to add links, and choose between permanent and temporary storage options. The temporary links are accompanied by a countdown timer, offering users control over the link's availability.

## Files and Directory Structure
#### Static
- lyncsync.png and link_favicon.png: These images serve as the logo for the website and favicon respectively.
I designed the logo of the website using an AI logo generator, this was an easy task and did not requrie much effort.
- Styles.css: This CSS file defines the styling for the website, ensuring a clean and user-friendly interface. It plays a crucial role in determining the overall look and feel of the application. I tried out various types of colors and layout styles to select the best design for the website. i decided to use the colors of the logo as the colors of the website, I set the same background color for the nav bar as the logo background color to have an elegant visual appeal. I used a purple color as the background color for the body as this was the color that was used for the link icon that was used as my favicon. I set the color for the uploaded links as white matching the remaining elements such as the select inputs. I made the nav bar headings such as log in, register, and log out bold in white as it suited the website's design. In the body i used black color for the headings "Add a link" and "All links". Overall, I am satisfied with my website's design, all the colors used resemble the colors used in the logo which makes it look aesthetic. Styling the website wasn't difficult as i used simlar styling from the birhtdays project.

#### Templates
- Layout.html: Defines the overall structure of the website layout, including the navigation bar, headers, and footers, ensuring consistency across pages. This was easy to make as I used the same layout from the finance project and made some changes.
- apology.html: This HTML template is utilized to render apology messages in case of errors during login or registration, providing a standardized way to communicate issues to users.
- index.html: The primary HTML template for the main page, includes a form for adding links, a table for displaying existing links, and JavaScript code for implementing countdown timers. I spent a lot of time trying to understand how the countdown timer worked and how i can delete the row once it is expired, I debated adding this feature because i was not able to get it to work as expected but finally after reading other materials i was able to implement it.
- login.html: Responsible for rendering the login page, including a form for user login with fields for username and password.
- registration.html: The HTML template for the user registration page, providing a form for users to create a new account.

#### App.py
The main Python script configures and runs the Flask web application, handling routes, user authentication, link addition, and expiration logic. Notable functions include:
- delete_expired_links(): Deletes expired links from the database. I used sql for this function as the temporary link had to be deleted.
- index(): The route for the main page, responsible for handling link addition, deletion, and rendering the main page. This was the hardest part of the application as I struggled a lot to delete the temporary link from the sql database. I realised the problem which was that the delete function was being called right after a temporary link was added and the condition for delete_expired_links was that the current time had to be less than the created_at+expiration_time for it to execute but as it was gettign executed immediately aftr the temporary link is added, i decided to use the time.sleep(expiration_time) method to execute the delete function after the expiration time which is when it started working as expected.
- login(): The route for user login, handling authentication and rendering the login page.
- logout(): The route for user logout, clearing the session, and redirecting to the login page.
- register(): The route for user registration, handling account creation and rendering the registration page.
The login, logout, and register functions were easy to make as I already have prior exeprience from the finance project.

#### helpers.py
- Provides helper functions used in the Flask application. The apology() function renders apology messages, and the login_required decorator ensures that certain routes are only accessible to authenticated users.

#### lyncsync.db
- The SQLite database file containing tables for storing user information and links. It includes two tables:
- users: Stores user information, including an user ID, username, and hashed password. Initially I made the mistake of having all of the link information in the same table, this caused some trouble and I later created the users_links table to separate the information.
- users_links: Stores link-related data, including a link ID, the link itself, associated device, user ID (foreign key referencing users), expiration type, expiration time, and creation time. Initially i did not store the time at which the link was added to the created_at row in my sql table, I later realised i required that information to compare the expiry of the link and added it.

## Design Choices and Considerations

#### Countdown Timer Implementation
Challenge: Implementing independent countdown timers for each temporary link.

Design Choice: JavaScript embedded in the index.html template provides individual scripts for each link, ensuring independent timers. The countdown updates every second, displaying minutes and seconds until expiration. When a temporary link expires, the corresponding table row is dynamically removed.

#### Styling and Layout
Challenge: Creating a visually appealing and responsive design for various devices.

Design Choice: The styles.css file defines a clean and user-friendly interface, while Bootstrap ensures responsiveness, making the application accessible across devices.

#### Database Structure
Challenge: Designing an effective database structure for user information and links.

Design Choice: SQLite database (lyncsync.db) includes two tables connected by a foreign key relationship. This structure allows the association of links with their respective users while ensuring data integrity.

#### User Authentication
Challenge: Ensuring secure user authentication.

Design Choice: User authentication is handled using Flask sessions, and the login_required decorator ensures that certain routes are only accessible to authenticated users.

## How to Launch Application
1. Clone the repository: https://github.com/code50/124700787.git
2. Change directory to project: cd project
3. Ensure that flask is installed: pip install flask
4. Run the application: flask run
5. Explore the application: Open the web browser and navigate to the provided url





