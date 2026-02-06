import sys
import os

def show_help():
    help_text = """
====================================================
      Faculty Finder: Team_VK Project CLI
====================================================
Usage: python manage.py [command]

Available Commands:
  //help          - Show this help menu
  run            - Start the FastAPI server
  stats          - Show database and faculty statistics
  docker         - Show Docker status and commands

Example: python manage.py //help
====================================================
    """
    print(help_text)

def start_server():
    print("Launching Faculty Finder API...")
    os.system("python run.py")

def show_stats():
    print("\n--- Project Statistics ---")
    os.system("python -c \"import sqlite3; conn = sqlite3.connect('faculty.db'); cursor = conn.cursor(); print(f'Database Total: {cursor.execute(\\\"SELECT COUNT(*) FROM faculty\\\").fetchone()[0]} faculty members'); conn.close()\"")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "//help":
        show_help()
    elif cmd == "run":
        start_server()
    elif cmd == "stats":
        show_stats()
    else:
        print(f"Unknown command: {cmd}")
        show_help()

if __name__ == "__main__":
    main()
