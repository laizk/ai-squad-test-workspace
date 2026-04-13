import argparse
import json
from typing import List, Dict, Optional


class Note:
    def __init__(self, title: str, content: str, tags: List[str], created_at: str = None):
        self.title = title
        self.content = content
        self.tags = tags
        self.created_at = created_at or ""

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Note':
        note = cls(
            title=data["title"],
            content=data["content"],
            tags=data["tags"],
            created_at=data.get("created_at", "")
        )
        return note


class NotesOrganizer:
    def __init__(self):
        self._notes: Dict[str, Note] = {}
        self._next_id: int = 1

    def add_note(self, title: str, content: str, tags: List[str]) -> Note:
        note = Note(
            title=title,
            content=content,
            tags=tags,
            created_at=""
        )
        self._notes[note.title] = note
        return note

    def list_notes(self) -> List[Note]:
        return list(self._notes.values())

    def list_by_tag(self, tag: str) -> List[Note]:
        return [note for note in self._notes.values() if tag in note.tags]

    def search_notes(self, query: str) -> List[Note]:
        query_lower = query.lower()
        return [
            note for note in self._notes.values()
            if query_lower in note.title.lower() or query_lower in note.content.lower()
        ]

    def delete_note(self, title: str) -> bool:
        if title in self._notes:
            del self._notes[title]
            return True
        return False

    def get_all_notes_dict(self) -> Dict[str, Dict]:
        return {title: note.to_dict() for title, note in self._notes.items()}


def main():
    parser = argparse.ArgumentParser(description="Notes Organizer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add_note command
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("title", help="Note title")
    add_parser.add_argument("content", help="Note content")
    add_parser.add_argument("--tags", nargs="*", default=[], help="Tags for the note")

    # list command
    subparsers.add_parser("list", help="List all notes")

    # list-by-tag command
    list_tag_parser = subparsers.add_parser("list-by-tag", help="List notes by tag")
    list_tag_parser.add_argument("tag", help="Tag to filter by")

    # search command
    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("query", help="Search query")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("title", help="Title of note to delete")

    # export command
    export_parser = subparsers.add_parser("export", help="Export all notes to JSON")

    args = parser.parse_args()

    organizer = NotesOrganizer()

    if args.command == "add":
        note = organizer.add_note(args.title, args.content, args.tags)
        print(f"Added note: {note.title}")

    elif args.command == "list":
        notes = organizer.list_notes()
        for note in notes:
            print(f"Title: {note.title}")
            print(f"Content: {note.content}")
            print(f"Tags: {', '.join(note.tags)}")
            print("---")

    elif args.command == "list-by-tag":
        notes = organizer.list_by_tag(args.tag)
        if notes:
            for note in notes:
                print(f"Title: {note.title}")
                print(f"Content: {note.content}")
                print(f"Tags: {', '.join(note.tags)}")
                print("---")
        else:
            print(f"No notes found with tag: {args.tag}")

    elif args.command == "search":
        notes = organizer.search_notes(args.query)
        if notes:
            for note in notes:
                print(f"Title: {note.title}")
                print(f"Content: {note.content}")
                print(f"Tags: {', '.join(note.tags)}")
                print("---")
        else:
            print(f"No notes found matching: {args.query}")

    elif args.command == "delete":
        if organizer.delete_note(args.title):
            print(f"Deleted note: {args.title}")
        else:
            print(f"Note not found: {args.title}")

    elif args.command == "export":
        notes_dict = organizer.get_all_notes_dict()
        print(json.dumps(notes_dict, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
