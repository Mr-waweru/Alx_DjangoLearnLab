# advanced-api-project

### api/serializer.py
**BookSerializer:**
- Serializes all fields of the Book model.
- Handles custom validation for publication_year to ensure data integrity (i.e., publication year is not in the future).
- Ensures books can be serialized independently or nested within another serializer.

**AuthorSerializer:**
- Serializes the `Author` model, focusing on the name field.
- Includes a nested serializer (BookSerializer) to dynamically serialize all books associated with the author.
- The `source="books"` links this field to the `related_name="books"` defined in the Book model's ForeignKey.

## Handling the Relationship Between Author and Book in Serializers:
**Forward Relationship:**
- In the `BookSerializer`, the author field represents the relationship to the Author model.
- The ForeignKey ensures that each book is linked to a specific author.

**Reverse Relationship:**
- In the AuthorSerializer, the books field uses the `related_name="books"` defined in the Book model.
- The `many=True` parameter in BookSerializer ensures that multiple related books can be serialized as a list.
- The `read_only=True` ensures that these books cannot be directly modified from the AuthorSerializer.
