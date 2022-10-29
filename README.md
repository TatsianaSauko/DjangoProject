# Django online bookstore repository
Short description: The buyer can navigate though the pages of the store, select
the desired section, study the product of interest in more detail and put it in
the cart. In addition, it is possible to place an order, apply a coupon to the
order. The buyer has the opportunity to cancel the order if it is in the "new"
status. Search for a product by title, the year of publishing, author,
description. There is also on the site there is sorting by price and by name.
Implemented registration, authorization, password recovery and login via Google.
### Installation (for users of operating systems of the Windows):

  1. Create a virtual environment
  2. git clone https://github.com/TatsianaSauko/DjangoProject.git
  3. cd DjangoProject/myshop
  4. pip install -r requirements.txt
  5. python manage.py migrate
  6. python manage.py runserver