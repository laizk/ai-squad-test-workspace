import pytest
from notes_organizer import Note, NotesOrganizer


class TestNote:
    def test_note_creation(self):
        note = Note(title="Test", content="Hello", tags=["test"])
        assert note.title == "Test"
        assert note.content == "Hello"
        assert note.tags == ["test"]

    def test_note_to_dict(self):
        note = Note(title="Test", content="Hello", tags=["test"])
        data = note.to_dict()
        assert data["title"] == "Test"
        assert data["content"] == "Hello"
        assert data["tags"] == ["test"]

    def test_note_from_dict(self):
        data = {
            "title": "Restored Note",
            "content": "This is restored content",
            "tags": ["restored", "tag2"],
            "created_at": "2024-01-01"
        }
        note = Note.from_dict(data)
        assert note.title == "Restored Note"
        assert note.content == "This is restored content"
        assert note.tags == ["restored", "tag2"]
        assert note.created_at == "2024-01-01"


class TestNotesOrganizer:
    def setup_method(self):
        self.organizer = NotesOrganizer()

    def test_add_note(self):
        note = self.organizer.add_note("My Note", "Content here", ["tag1"])
        assert note.title == "My Note"
        assert note.content == "Content here"
        assert note.tags == ["tag1"]

    def test_list_notes(self):
        self.organizer.add_note("Note 1", "Content 1", ["tag1"])
        self.organizer.add_note("Note 2", "Content 2", ["tag2"])
        notes = self.organizer.list_notes()
        assert len(notes) == 2
        assert any(n.title == "Note 1" for n in notes)
        assert any(n.title == "Note 2" for n in notes)

    def test_list_by_tag(self):
        self.organizer.add_note("Note 1", "Content 1", ["tag1", "tag2"])
        self.organizer.add_note("Note 2", "Content 2", ["tag2"])
        notes = self.organizer.list_by_tag("tag2")
        assert len(notes) == 2
        assert all("tag2" in n.tags for n in notes)

    def test_search_notes(self):
        self.organizer.add_note("Hello World", "This is a test", ["test"])
        self.organizer.add_note("Goodbye World", "Another test", ["test"])
        notes = self.organizer.search_notes("world")
        assert len(notes) == 2

    def test_search_notes_by_content(self):
        self.organizer.add_note("My Title", "Search this content", ["search"])
        notes = self.organizer.search_notes("content")
        assert len(notes) == 1
        assert notes[0].title == "My Title"

    def test_delete_note(self):
        self.organizer.add_note("To Delete", "Content to delete", ["delete"])
        result = self.organizer.delete_note("To Delete")
        assert result is True
        notes = self.organizer.list_notes()
        assert len(notes) == 0

    def test_delete_nonexistent_note(self):
        result = self.organizer.delete_note("Nonexistent")
        assert result is False

    def test_get_all_notes_dict(self):
        self.organizer.add_note("Note A", "Content A", ["tag1"])
        self.organizer.add_note("Note B", "Content B", ["tag2"])
        notes_dict = self.organizer.get_all_notes_dict()
        assert "Note A" in notes_dict
        assert "Note B" in notes_dict
        assert notes_dict["Note A"]["title"] == "Note A"
        assert notes_dict["Note A"]["content"] == "Content A"
        assert notes_dict["Note A"]["tags"] == ["tag1"]
        assert notes_dict["Note B"]["title"] == "Note B"
        assert notes_dict["Note B"]["content"] == "Content B"
        assert notes_dict["Note B"]["tags"] == ["tag2"]

    def test_empty_notes_dict(self):
        notes_dict = self.organizer.get_all_notes_dict()
        assert notes_dict == {}

    def test_add_note_with_empty_tags(self):
        note = self.organizer.add_note("Empty Tags", "Content", [])
        assert note.tags == []

    def test_search_notes_empty(self):
        notes = self.organizer.search_notes("nonexistent")
        assert len(notes) == 0
