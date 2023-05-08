# Demo
This is sample of what django-easy-faq can look like with [Bootstrap 5](https://getbootstrap.com/) styled templates.
This is here to demonstrate what this django app provides and what features it supports.
Below is some screenshots with the default settings and of what it looks like with some of the other settings turned on. 

### with no settings

This is for a user that is logged in when the faq app has no settings set.

/faq/
![image](default-1.png)
/faq/category-1/
![image](default-2.png)
/faq/category-1/do-you-offer-any-discounts-or-promotions/
![image](default-3.png)
with an answer
![image](default-4.png)
### no_category_description

Categories don't have category descriptions.

/faq/
![image](option-1-1.png)

/faq/category-1/
![image](option-1-2.png)
### no_category

there are no categories for questions. All questions show on the faq index page

/faq/
![image](option-2-1.png)

/faq/do-you-offer-any-discounts-or-promotions/
![image](option-2-2.png)

### logged_in_users_can_add_question

allow logged in users to ask questions

/faq/category-1/
![image](option-3-1.png)

/faq/category-1/add/question/
![image](option-3-2.png)

### logged_in_users_can_answer_question

allow users that are logged in to be able to answer the questions

/faq/category-1/what-payment-methods-do-you-accept/
![image](option-4-1.png)

/faq/category-1/what-payment-methods-do-you-accept/answer/
![image](option-4-2.png)

### allow_multiple_answers

More than one answer can exist for the question. If `logged_in_users_can_answer_question` is also set then users can add their own answers to the question.

/faq/category-1/what-is-your-return-policy/
![image](option-5-1.png)

### no_comments

showing or adding comments to questions is removed

/faq/category-1/do-you-offer-any-discounts-or-promotions/
![image](option-6-1.png)

### anonymous_user_can_comment

even users that are not logged in can comment

/faq/category-1/do-you-offer-any-discounts-or-promotions/
![image](default-3.png)

### view_only_comments

users can only view the comments

/faq/category-1/do-you-offer-any-discounts-or-promotions/
![image](option-8-1.png)

### no_votes

users cannot vote on questions or answers

/faq/category-1/do-you-offer-any-discounts-or-promotions/
![image](option-9-1.png)

### no_answer_votes

can only vote on questions

/faq/category-1/do-you-offer-any-discounts-or-promotions/
![image](option-10-1.png)

### no_question_votes

can only vote on answers

/faq/category-1/do-you-offer-any-discounts-or-promotions/
![image](option-11-1.png)
