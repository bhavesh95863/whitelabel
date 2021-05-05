ERPNext Whitelabel

This app have following features:
1. Change App logo
2. Change Favicon
3. Change Splash Image
4. Hide Help Menu
5. Hide powered by text from the website
6. remove welcome page
7. update welcome blog post
8. App logo size adjusts from Whitelabel setting page
9. Update onboard steps for remove video and documentation link(Version13)
10. Navbar Background color manage from Whitelabel setting.
11. Custom Navbar Title and CSS for title Manage from Whitelabel setting.
12. Change Login Page Title From Whitelabel Setting Page(https://github.com/bhavesh95863/whitelabel/issues/7)


Whitelabel Setting Page
![image](https://user-images.githubusercontent.com/34086262/115605632-5e28ed00-a300-11eb-986d-5114ef128de3.png)

Custom Navbar Title
![image](https://user-images.githubusercontent.com/34086262/115721516-bc56de00-a39b-11eb-94b3-787b0481fb60.png)

Below are important setting in whitelabel setting page.
1. Ignore Onboard Whitelabel:<br/>
   If this setting value true then this app will not whitelabel onboarding steps and onboarding modules.
2. Show help menu:<br/>
   By default this app hide help menu. this setting show help menu if value of this setting true.
3. Disable New Update Popup:<br/>
  If this setting value true then it will disable new updates popup.


Installation Steps:<br/>
1. bench get-app https://github.com/bhavesh95863/whitelabel<br/>
2. bench --site sitename install-app whitelabel<br/>
3. bench migrate<br/>
4. bench restart<br/>
5. bench clear-cache


Note:
You need to upload your logo at /public/images

If any issue or suggestion do write in the issue list we will resolve that.
