import sys
import scraper

# Kann verwendet werden um den scraper über die CLI auszuführen
# Beispiel: python scraper_via_cli.py category1 category2 category3
# Praktisch: py scrpaper_via_cli.py (cat categories)

def main():
    
    categories = sys.argv[1:] 

    if not categories:
        print("Error: No categories provided. Please provide at least one category.")
        sys.exit(1)

    print(f"Categories to scrape: {categories}")

    scraper.scrape_main(categories)

if __name__ == "__main__":
    main()