# Simple web app to monitor employee working hours and their task
A simple app for employee work hours management

In this app we have 3 types of accounts permissions: Admin/owner, management, employee. Each permissions have its own "part" of app with permissions to enter. Employee can not access management part and so on.
App was created to monitor where and for how long each employee worked in certain days.
![image](https://user-images.githubusercontent.com/90956337/229802985-ffe23d5b-ccfb-4af7-9aef-19793b165da8.png)

By clicking 'rozpocznij prace' we creating database entry about given day, mostly is today(). After creating our working day we can add task and modify then. Beside some minors securities like imposibility to end work day without ending all the task we added, we also check if we do not have day started yesterday(assuming night shift).
Management have access to all sort of filters, and task, project that are working on today:

![image](https://user-images.githubusercontent.com/90956337/229804411-2478e7ba-e8fd-4e32-906e-69f96757893f.png)
![image](https://user-images.githubusercontent.com/90956337/229805687-ba1cd0e6-704b-4e57-a200-0387fa7e7449.png)

They can manipulate dates, employees and projects to see who had been working on certain task and where to their needs.
Also they have access to overhour tab, in which they can see how much overhours certains workes accuired. 
