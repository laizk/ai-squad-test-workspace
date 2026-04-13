from dataclasses import dataclass, field
from typing import List, Optional
import argparse
from datetime import datetime


@dataclass
class Note:
    """Represents a markdown note with metadata."""
    title: str
    content: str
    tags: List[str]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class NotesManager:
    """Manages a collection of notes stored in memory."""
    
    def __init__(self):
        self._notes: dict[str, Note] = {}
    
    def add_note(self, title: str, content: str, tags: List[str]) -> Note:
        """Add a new note to the collection.
        
        Args:
            title: The note title
            content: The markdown content
            tags: List of tags for categorization
            
        Returns:
            The created Note object
        """
        note = Note(title=title, content=content, tags=tags)
        self._notes[title] = note
        return note
    
    def list_by_tag(self, tag: str) -> List[Note]:
        """List all notes containing the specified tag.
        
        Args:
            tag: The tag to filter by
            
        Returns:
            List of Note objects with the given tag
        """
        return [note for note in self._notes.values() if tag in note.tags]
    
    def search_titles(self, query: str) -> List[Note]:
        """Search note titles and tags for the given query string.
        
        Args:
            query: The search query (case-insensitive substring match)
            
        Returns:
            List of Note objects whose titles or tags contain the query
        """
        query_lower = query.lower()
        return [note for note in self._notes.values() 
                if query_lower in note.title.lower() or 
                   any(query_lower in tag.lower() for tag in note.tags)]
    
    def get_note(self, title: str) -> Optional[Note]:
        """Get a note by title.
        
        Args:
            title: The note title
            
        Returns:
            The Note object or None if not found
        """
        return self._notes.get(title)


def main():
    """CLI entrypoint for the notes organizer."""
    manager = NotesManager()
    
    parser = argparse.ArgumentParser(
        description='Notes Organizer CLI - Manage markdown notes'
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add note command
    add_parser = subparsers.add_parser('add', help='Add a new note')
    add_parser.add_argument('--title', required=True, help='Note title')
    add_parser.add_argument('--content', required=True, help='Note content (markdown)')
    add_parser.add_argument('--tags', required=True, help='Comma-separated tags')
    
    # List by tag command
    list_parser = subparsers.add_parser('list', help='List notes by tag')
    list_parser.add_argument('--tag', required=True, help='Tag to filter by')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search note titles')
    search_parser.add_argument('--query', required=True, help='Search query')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        tags = [t.strip() for t in args.tags.split(',') if t.strip()]
        note = manager.add_note(args.title, args.content, tags)
        output = f"Added note: {note.title}\nTags: {', '.join(note.tags)}\nCreated: {note.created_at}"
        print(output)
    
    elif args.command == 'add':
        tags = [t.strip() for t in args.tags.split(',') if t.se
        note = manager.add_note(args.title, args.content, tags)
        print(f"Added note: {note.title}")
        print(f"Tags: {', '.join(note.tags)}")
        print(f"Created: {note.created_at}")
    
    elif args.command == 'list':
        notes = manager.list_by_tag(args.tag)
        if notes:
            for note in notes:
                print(f"\nTitle: {note.title}")
                print(f"Content:\n{note.content}")
                print(f"Tags: {', '.join(note.tags)}")
        else:".strip() if t.strip()]
        note = manager.add_note(args.title, args.content, tags)
        print(f"Added note: {note.title}")
        print(f"Tags: {', '.join(note.tags)}")
        print(f"Captured: {note.created_at}")
    
    elif args.command == 'list':
        notes = manager.list_by_tag(args.tag)
        if notes:
            for note in notes:
                print(f"\nTitle: {note.title}")
                print(f"Content:\n{note.content}")
                says "Captured: {note.created_at}" instead of "Created: {note.created_at}"