from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.category import Category
from app import db
import os

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    首頁：顯示熱門或最新食譜。
    """
    recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes)

@recipe_bp.route('/search', methods=['GET', 'POST'])
def search():
    """
    食材搜尋。
    """
    ingredients = Ingredient.get_all()
    if request.method == 'POST':
        selected_ids = request.form.getlist('ingredients')
        if not selected_ids:
            flash('請至少勾選一項食材。', 'warning')
            return render_template('search/index.html', ingredients=ingredients)
        
        # 簡單的搜尋邏輯：找出包含至少一個選定食材的食譜
        # 進階邏輯可在 Model 中實作，這裡先做基礎過篩
        all_recipes = Recipe.get_all()
        results = []
        selected_ids = [int(i) for i in selected_ids]
        
        for r in all_recipes:
            recipe_ing_ids = [ing.id for ing in r.ingredients]
            intersection = set(selected_ids) & set(recipe_ing_ids)
            if intersection:
                # 計算匹配度 (選中的食材中有多少在食譜裡)
                match_count = len(intersection)
                results.append({'recipe': r, 'match_count': match_count})
        
        # 按匹配數量排序
        results.sort(key=lambda x: x['match_count'], reverse=True)
        return render_template('search/results.html', results=results)
        
    return render_template('search/index.html', ingredients=ingredients)

@recipe_bp.route('/recipe/create', methods=['GET', 'POST'])
@login_required
def create():
    """
    發佈食譜。
    """
    categories = Category.get_all()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        category_id = request.form.get('category_id')
        ingredient_names = request.form.get('ingredients', '').split(',')
        
        if not title or not instructions:
            flash('標題與步驟為必填項。', 'error')
            return render_template('recipe/create.html', categories=categories)
            
        # 處理食材 (如果不存在則建立)
        recipe_ingredients = []
        for name in ingredient_names:
            name = name.strip()
            if name:
                ing = Ingredient.get_by_name(name)
                if not ing:
                    ing = Ingredient.create(name=name)
                if ing:
                    recipe_ingredients.append(ing)
        
        # 建立食譜
        recipe = Recipe.create(
            title=title,
            instructions=instructions,
            author_id=current_user.id,
            description=description,
            category_id=category_id if category_id else None,
            ingredients=recipe_ingredients
        )
        
        if recipe:
            flash('食譜發佈成功！', 'success')
            return redirect(url_for('recipe.detail', id=recipe.id))
        else:
            flash('儲存失敗，請重試。', 'error')
            
    return render_template('recipe/create.html', categories=categories)

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """
    查看食譜詳情。
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜。', 'error')
        return redirect(url_for('recipe.index'))
    return render_template('recipe/detail.html', recipe=recipe)

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    """
    編輯食譜頁面。
    """
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe.author_id != current_user.id:
        flash('您無權編輯此食譜。', 'error')
        return redirect(url_for('recipe.index'))
    
    categories = Category.get_all()
    # 將食材清單轉回逗點分隔字串方便修改
    ing_str = ', '.join([ing.name for ing in recipe.ingredients])
    return render_template('recipe/edit.html', recipe=recipe, categories=categories, ingredients_meta=ing_str)

@recipe_bp.route('/recipe/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    """
    更新食譜。
    """
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe.author_id != current_user.id:
        flash('操作失敗。', 'error')
        return redirect(url_for('recipe.index'))
        
    title = request.form.get('title')
    description = request.form.get('description')
    instructions = request.form.get('instructions')
    category_id = request.form.get('category_id')
    ingredient_names = request.form.get('ingredients', '').split(',')
    
    # 處理食材更新
    new_ingredients = []
    for name in ingredient_names:
        name = name.strip()
        if name:
            ing = Ingredient.get_by_name(name)
            if not ing:
                ing = Ingredient.create(name=name)
            if ing:
                new_ingredients.append(ing)
    
    updated = Recipe.update(id, 
        title=title, 
        description=description, 
        instructions=instructions, 
        category_id=category_id if category_id else None,
        ingredients=new_ingredients
    )
    
    if updated:
        flash('更新成功！', 'success')
    else:
        flash('更新失敗。', 'error')
        
    return redirect(url_for('recipe.detail', id=id))

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """
    刪除食譜。
    """
    recipe = Recipe.get_by_id(id)
    if not recipe or recipe.author_id != current_user.id:
        flash('您無權執行此操作。', 'error')
        return redirect(url_for('recipe.index'))
        
    if Recipe.delete(id):
        flash('食譜已刪除。', 'info')
    else:
        flash('刪除失敗。', 'error')
        
    return redirect(url_for('recipe.index'))
