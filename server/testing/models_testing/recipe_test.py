import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe

class TestRecipe:
    '''Recipe in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
        
        with app.app_context():
            Recipe.query.delete()
            db.session.commit()

            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions=(
                    "Or kind rest bred with am shed then. In "
                    "raptures building and bringing be. Elderly is detract "
                    "tedious assured private so to visited. Do travelling "
                    "companions contrasted it. Mistress strongly remember "
                    "up to. Ham him compass you proceed calling detract. "
                    "Better of always missed we person Mr. September "
                    "smallness northward situation few her certainty something."
                ),
                minutes_to_complete=60,
            )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter_by(title="Delicious Shed Ham").first()

            assert new_recipe.title == "Delicious Shed Ham"
            assert new_recipe.minutes_to_complete == 60
            assert "companions contrasted" in new_recipe.instructions

    def test_requires_title(self):
        '''raises IntegrityError if title is missing.'''

        with app.app_context():
            Recipe.query.delete()
            db.session.commit()

            recipe = Recipe(
                title=None,
                instructions="A" * 60,
                minutes_to_complete=20
            )

            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''raises ValueError if instructions are less than 50 characters.'''

        with app.app_context():
            Recipe.query.delete()
            db.session.commit()

            with pytest.raises((ValueError, IntegrityError)):
                recipe = Recipe(
                    title="Short Ham",
                    instructions="Too short.",
                    minutes_to_complete=30
                )
                db.session.add(recipe)
                db.session.commit()
