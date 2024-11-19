# VendusAutomator

https://www.vendus.pt/

Vendus Automator is a tool that automates the generation of documents in the Vendus system based on the selection of services and quantities provided by the user. 

Using Selenium, the program logs into the system, navigates to the point-of-sale (POS) section, and generates documents such as invoices, based on the selected services.

Features: 

Automatic Login: The program automatically logs into the Vendus system using the provided credentials.

Service Selection: Users can choose the services to be issued and the quantity of each, including services like haircuts and beard grooming, with predefined prices.

Document Generation: Based on the selected services, the program generates the required documents through the Vendus POS system, using automatic printing to avoid dialog boxes.

How to Use
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/vendus-automator.git
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Configure your credentials: In the code, replace the CREDENTIALS values with your Vendus system credentials.

Run the script:

bash
Copy code
python vendus_automator.py

The program will prompt you to enter the quantity of services to be issued, such as (...)

The system will log in, open the POS system, and automatically generate the documents based on the quantities you entered.








