from typing import List, Optional


class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.id = id(self)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags
        }


class NotesOrganizer:
    def __init__(self):
        self.notes: List[Note] = []
    
    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Note:
        note = Note(title, content, tags)
        self.notes.append(note)
        return note
    
    def list_by_tag(self, tag: str) -> List[dict]:
        matching = [note.to_dict() for note in self.notes if tag in note.tags]
        return matching
    
    def search_titles(self, query: str) -> List[dict]:
        query_lower = query.lower()
        matching = [note.to_dict() for note in self.notes if query_lower in note.title.lower()]
        return matching
    
    def list_all(self) -> List[dict]:
        return [note.to_dict() for note in self.notes]
