from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Database:
    BASE = declarative_base()

    class Category(BASE):
        __tablename__ = 'categories'

        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(30), nullable=False)

        books = relationship('Book', back_populates='category')

    class Author(BASE):
        __tablename__ = 'authors'

        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(30), nullable=False)
        surname = Column(String(30), nullable=False)
        birth_date = Column(Date, nullable=False)
        nationality = Column(String(30), nullable=False)

        books = relationship('Book', back_populates='author')

    class User(BASE):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(30), nullable=False)
        surname = Column(String(30), nullable=False)
        birth_date = Column(Date, nullable=False)
        address = Column(String(30), nullable=False)
        phone_number = Column(String(30), nullable=True)

        books = relationship('Book', back_populates='user')

    class Book(BASE):
        __tablename__ = 'books'

        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String(30), nullable=False)
        published_date = Column(Date, nullable=False)
        language = Column(String(20), nullable=False)
        ISBN = Column(String(40), nullable=False)
        last_borrow = Column(Date, nullable=True)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
        category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
        author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

        author = relationship('Author', back_populates='books')
        category = relationship('Category', back_populates='books')
        user = relationship('User', back_populates='books')

    def __init__(self):
        self.engine = create_engine('mysql://user:lukasz@localhost:3306/library')
        self.BASE.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _object_add(self, object):
        self.session.add(object)
        self.session.commit()

    def category_add(self, name):
        new_category = self.Category(name=name)
        self._object_add(new_category)

    def author_add(self, name, surname, birth_date, nationality):
        new_author = self.Author(name=name, surname=surname, birth_date=birth_date, nationality=nationality)
        self._object_add(new_author)

    def book_add(self, title, published_date, language, ISBN, category_id, author_id):
        new_book = self.Book(title=title, published_date=published_date, language=language, ISBN=ISBN,
                             category_id=category_id, author_id=author_id)
        self._object_add(new_book)
