import pytest
from notes_organizer import Note, NotesOrganizer


class TestNote:
    def test_note_creation(self):
        note = Note("Test Title", "Test Content", ["tag1", "tag2"])
        assert note.title == "Test Title"
        assert note.content == "Test Content"
        assert note.tags == ["tag1", "tag2"]
    
    def test_note_without_tags(self):
        note = Note("Test Title", "Test Content")
        assert note.tags == []


class TestNotesOrganizer:
    def test_add_note(self):
        organizer = NotesOrganizer()
        note = organizer.add_note("My Note", "Content here", ["important"])
        assert len(organizer.notes) == 1
        assert note.title == "My Note"
    
    def test_list_by_tag(self):
        organizer = NotesOrganizer()
        organizer.add_note("Note 1", "Content 1", ["work"])
        organizer.add_note("Note 2", "Content 2", ["work", "personal"])
        organizer.add_note("Note 3", "Content 3", ["personal"])
        
        results = organizer.list_by_tag("work")
        assert len(results) == 2
        assert results[0]['title'] == "Note 1"
        assert results[1]['title'] == "Note 2"
    
    def test_search_titles(self):
        organizer = NotesOrganizer()
        organizer.add_note("Python Programming", "Learn Python")
        organizer.add_note("JavaScript Basics", "Learn JS")
        organizer.add_note("Java Development", "Learn Java")
        
        results = organizer.search_titles("python")
        assert len(results) == 1
        assert results[0]['title'] == "Python Programming"
    
    def test_search_titles_case_insensitive(self):
        organizer = NotesOrganizer()
        organizer.add_note("Python Programming", "Learn Python")
        
        results = organizer.search_titles("PYTHON")
        assert len(results) == 1
        assert results[0]['title'] == "Python Programming"
    
    def test_list_all(self):
        organizer = NotesOrganizer()
        organizer.add_note("Note 1", "Content 1")
        organizer.add_note("Note 2", "Content 2")
        
        results = organizer.list_all()
        assert len(results) == 2
        assert results[0]['title'] == "Note 1"
        assert results[1]['title'] == "Note 2"
