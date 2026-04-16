from app import create_app
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe

app = create_app()
with app.app_context():
    print("--- Ingredients ---")
    ings = Ingredient.query.all()
    for i in ings:
        print(f"ID: {i.id}, Name: {i.name}")
    
    print("\n--- Recipes ---")
    recs = Recipe.query.all()
    for r in recs:
        ing_list = [ing.name for ing in r.ingredients]
        print(f"Recipe: {r.title}, Ingredients: {ing_list}")
