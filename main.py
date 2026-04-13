import argparse
from notes_organizer import NotesOrganizer


def main():
    parser = argparse.ArgumentParser(description="Notes Organizer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add note command
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("title", help="Note title")
    add_parser.add_argument("content", help="Note content")
    add_parser.add_argument("--tags", nargs="*", default=[], help="Tags for the note")
    
    # List by tag command
    tag_parser = subparsers.add_parser("list-tag", help="List notes by tag")
    tag_parser.add_argument("tag", help="Tag to filter by")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search note titles")
    search_parser.add_argument("query", help="Search query")
    
    # List all command
    list_parser = subparsers.add_parser("list", help="List all notes")
    
    args = parser.parse_args()
    
    organizer = NotesOrganizer()
    
    if args.command == "add":
        note = organizer.add_note(args.title, args.content, args.tags)
        print(f"Added note: {note.title}")
        print(f"Tags: {note.tags}")
    
    elif args.command == "list-tag":
        results = organizer.list_by_tag(args.tag)
        if results:
            for note in results:
                print(f"[{note['title']}] {note['content']} | Tags: {', '.join(note['tags'])}")
        else:
            print(f"No notes found with tag: {args.tag}")
    
    elif args.command == "search":
        results = organizer.search_titles(args.query)
        if results:
            for note in results:
                print(f"[{note['title']}] {note['content']}")
        else:
            print(f"No notes found matching: {args.query}")
    
    elif args.command == "list":
        results = organizer.list_all()
        if results:
            for note in results:
                print(f"[{note['title']}] {note['content']} | Tags: {', '.join(note['tags'])}")
        else:
            print("No notes found.")


if __name__ == "__main__":
    main()
