#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Book

engine = create_engine('sqlite:///readinglist.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add Example User
sampleUser = User(name='SampleUser')
session.add(sampleUser)
session.commit()

userID = sampleUser.id

# Add Example Books
sampleBook1 = Book(
    title='La Belle Sauvage',
    author='Philip Pullman',
    genre='Children-Young Adult',
    description="""
        Continuation of Pullman's 'His Dark Materials' trilogy.
        Tells the story of how the infant Lyra gained sanctuary at Oxford.
        """,
    user_id=userID)
session.add(sampleBook1)
session.commit()

sampleBook2 = Book(
    title='Death: The Deluxe Edition',
    author='Neil Gaiman',
    genre='Graphic Novel',
    description="""
        An omnibus edition of the graphic novels focusing on the Endless Death.
        (A spin off from Neil Gaiman's Sandman graphic novels)
        """,
    user_id=userID)
session.add(sampleBook2)
session.commit()

sampleBook3 = Book(
    title='The Sandman: Endless Nights',
    author='Neil Gaiman',
    genre='Graphic Novel',
    description="""
        A follow up to Neil Gaiman's Sandman series.
        Consists of seven stories, each focused on a different Endless.
        """,
    user_id=userID)
session.add(sampleBook3)
session.commit()

sampleBook4 = Book(
    title='A Study in Scarlet',
    author='Sir Arthur Conan Doyle',
    genre='Classic',
    description="""
        The first appearance of Sherlock Holmes and Dr Watson.
        """,
    user_id=userID)
session.add(sampleBook4)
session.commit()

sampleBook5 = Book(
    title="A Connecticut Yankee in King Arthur's Court",
    author='Mark Twain',
    genre='Classic',
    description="""
        A 19th century man is knocked back in time to Camelot via head injury.
        He goes about attempting to industrialize and Amercanize Camelot.
        """,
    user_id=userID)
session.add(sampleBook5)
session.commit()

sampleBook6 = Book(
    title="Assassin's Apprentice",
    author='Robin Hobb',
    genre='Fantasy',
    description="""
        First book of the Farseer Trilogy.
        Covers the early life of FitzChivalry as he trains as an assassin.
        """,
    user_id=userID)
session.add(sampleBook6)
session.commit()

sampleBook7 = Book(
    title="""
        Good Omens: The Nice and Accurate Prophecies of Agnes Nutter, Witch
        """,
    author='Neil Gaiman and Terry Pratchett',
    genre='Fantasy',
    description='An angel and a demon team up to avert the Apocalypse.',
    user_id=userID)
session.add(sampleBook7)
session.commit()

sampleBook8 = Book(
    title='Small Gods',
    author='Terry Pratchett',
    genre='Fantasy',
    description="""
        Tells the story of the Great God Om and his prophet Brother Brutha.
        """,
    user_id=userID)
session.add(sampleBook8)
session.commit()

sampleBook9 = Book(
    title='At the Mountains of Madness',
    author='H.P. Lovecraft',
    genre='Horror',
    description="""
        An expedition to the Antarctic meets with ancient horror.
        """,
    user_id=userID)
session.add(sampleBook9)
session.commit()

sampleBook10 = Book(
    title='The Damnation Game',
    author='Clive Barker',
    genre='Horror',
    description="""
        A man attempts to avoid fullfilling his pact with a supernatural being.
        """,
    user_id=userID)
session.add(sampleBook10)
session.commit()

sampleBook11 = Book(
    title='Altered Carbon',
    author='Richard Morgan',
    genre='SciFi',
    description="""
        In the future, minds can be stored and downloaded to new bodies.
        When a rich man dies, he hires an elite soldier to investigate.
        """,
    user_id=userID)
session.add(sampleBook11)
session.commit()

sampleBook12 = Book(
    title='Revelation Space',
    author='Alastair Reynolds',
    genre='SciFi',
    description="""
        First book in the Revelation Space series.
        An archaeologist studies the destruction of an alien race.
        A spaceship crew search to cure their captain of a nanotech virus.
        An assassin is sent to kill the archaeologist.
        """,
    user_id=userID)
session.add(sampleBook12)
session.commit()

sampleBook13 = Book(
    title='Books of Blood',
    author='Clive Barker',
    genre='Anthology',
    description="""
        A collection of horror stories by Clive Barker.
        """,
    user_id=userID)
session.add(sampleBook13)
session.commit()

sampleBook14 = Book(
    title='From the Borderlands',
    author='Various',
    genre='Anthology',
    description="""
        A collection of suspense, horror and dark fantasy stories.
        """,
    user_id=userID)
session.add(sampleBook14)
session.commit()

sampleBook15 = Book(
    title='Magic Terror',
    author='Peter Straub',
    genre='Anthology',
    description="""
        A collection of horror and dark fantasy tales by Peter Straub.
        """,
    user_id=userID)
session.add(sampleBook15)
session.commit()

sampleBook16 = Book(
    title='100 Wild Little Weird Tales',
    author='Various',
    genre='Anthology',
    description="""
        A collection of the best stories from the 'Weird Tales' magazine.
        """,
    user_id=userID)
session.add(sampleBook16)
session.commit()

sampleBook17 = Book(
    title='The Tao of Pooh',
    author='Benjamin Hoff',
    genre='Non-Fiction',
    description="""
        Daoist philosophy explained through Winnie the Pooh.
        """,
    user_id=userID)
session.add(sampleBook17)
session.commit()

sampleBook18 = Book(
    title='Steamed',
    author='Katie MacAlister',
    genre='Romance',
    description="""
        Jack Fletcher is transported to a steampunk alternate reality.
        There he gets entagled with Octavia Pye, an airship captain.
        Adventure and romance ensue.
        """,
    user_id=userID)
session.add(sampleBook18)
session.commit()

sampleBook19 = Book(
    title='Cover Her Face',
    author='P.D. James',
    genre='Mystery-Crime',
    description="""
        DCI Adam Dalgliesh investigates the murder of a maid at a manor house.
        """,
    user_id=userID)
session.add(sampleBook19)
session.commit()

sampleBook20 = Book(
    title='Gaudy Night',
    author='Dorothy L. Sayers',
    genre='Mystery-Crime',
    description="""
        The 10th Lord Peter Wimsey mystery.
        Vandalism and poison pen letters threaten scandal at Oxford.
        Lord Peter Wimsey and Harriet Vane investigate.
        """,
    user_id=userID)
session.add(sampleBook20)
session.commit()

sampleBook21 = Book(
    title='And Then There Were None',
    author='Agatha Christie',
    genre='Mystery-Crime',
    description="""
        Most popular Agatha Christie novel and the author's favorite.
        Eight people are invited to an isolated island off the Devon coast.
        In the first night, all are accused of having gotten away with murder.
        One by one they begin to die as they try to unravel who is responsible.
        """,
    user_id=userID)
session.add(sampleBook21)
session.commit()

sampleBook22 = Book(
    title='Frost: Poems',
    author='Robert Frost',
    genre='Poetry',
    description="""
        A collection of poetry from several of Robert Frost's books.
        """,
    user_id=userID)
session.add(sampleBook22)
session.commit()

sampleBook23 = Book(
    title='Where the Sidewalk Ends: 30th Anniversary Edition',
    author='Shel Silverstein',
    genre='Poetry',
    description="""
        Award-winning collection of poetry by Shel Silverstein.
        Contains 12 new poems not published in previous editions.
        """,
    user_id=userID)
session.add(sampleBook23)
session.commit()

print("Sample Data added.")
