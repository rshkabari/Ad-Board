import datetime
from colorama import Fore, init
from user import User
from ad import Ad
from ad_board import AdBoard

init(autoreset=True)  # Initialize colorama for colored text

def main():
    ad_board = AdBoard()

    while True:
        print("\nAd Board Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Post an ad")
        print("4. Edit an ad")
        print("5. View my ads")
        print("6. Delete an ad")
        print("7. View all ads")
        print("8. Search ads by keyword")
        print("9. Logout")
        print("10. Quit")

        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            ad_board.register(username, password)
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            ad_board.login(username, password)
        elif choice == "3":
            title = input("Enter ad title: ")
            description = input("Enter ad description: ")
            contact_info = input("Enter contact information: ")
            category = input("Enter ad category: ")
            ad_board.post_ad(title, description, contact_info, category)
        elif choice == "4":
            ad_id = int(input("Enter the ID of the ad you want to edit: "))
            title = input("Enter new ad title: ")
            description = input("Enter new ad description: ")
            contact_info = input("Enter new contact information: ")
            category = input("Enter new ad category: ")
            ad_board.edit_ad(ad_id, title, description, contact_info, category)
        elif choice == "5":
            ad_board.view_my_ads()
        elif choice == "6":
            ad_id = int(input("Enter the ID of the ad you want to delete: "))
            ad_board.delete_ad(ad_id)
        elif choice == "7":
            page = int(input("Enter the page number: "))
            sort_by = input("Sort by (timestamp or category): ").lower()
            keyword = input("Enter keyword to search (leave blank for all ads): ").strip()
            ad_board.view_ads(page, sort_by, keyword)
        elif choice == "8":
            keyword = input("Enter keyword to search ads: ")
            ad_board.search_ads_by_keyword(keyword)
        elif choice == "9":
            ad_board.logout()
        elif choice == "10":
            ad_board.quit()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
