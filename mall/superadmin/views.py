#coding=utf-8
from flask import Blueprint, flash, redirect, render_template, request, url_for,current_app
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from flask_login import current_user

from .models import SystemVersion,Category,BaseProducts
from mall.utils import templated,flash_errors,allowed_file,gen_rnd_filename
from . import blueprint
from .forms import AddCategoryForm,AddBaseProductForm

import datetime as dt
import os

@blueprint.route('/')
@templated()
def home():
    print(current_app.config['WECHAT_APPID'])
    return dict()


@blueprint.route('/all_version')
@templated()
def all_version():
	return dict(version=SystemVersion.query.order_by(desc('id')).all())


@blueprint.route('/add_version',methods=['POST'])
def add_version_post():
	SystemVersion.create(
		number=request.form.get('number',' '),
		title=request.form.get('title',' '),
		summary=request.form.get('summary',' '),
		context=request.form.get('context',' '),	
	)
	flash('添加完成.','success')
	return redirect(url_for('.all_version'))


#分类
@blueprint.route('/category')
@templated()
def category():
	return dict(categorys=Category.query.order_by('sort').all())

#分类
@blueprint.route('/add_category')
@templated()
def add_category():
	return dict(form=AddCategoryForm())


@blueprint.route('/add_category',methods=["POST"])
def add_category_post():
	form=AddCategoryForm(request.form)
	if form.validate_on_submit():
		if form.pid.data==-1:
			form.pid.data=None
			
		Category.create(
			name=form.name.data,
			ico=form.ico.data,
			sort=form.sort.data,
			parent_id=form.pid.data,
			active=True,			
		)
		flash('添加成功','success')
		return redirect(url_for('.add_category'))
	else:
		flash('添加失败','danger')
		flash_errors(form)
	return redirect(url_for('.add_category'))


#商品基础数据
@blueprint.route('/base_products')
@templated()
def base_products():
	base_product = BaseProducts.query.all()
	return dict(base_product=base_product)


#添加商品基础数据
@blueprint.route('/add_base_product')
@templated()
def add_base_product():

	return dict(form=AddBaseProductForm())


@blueprint.route('/add_base_product',methods=['POST'])
def add_base_product_post():
    form=AddBaseProductForm()
    if form.validate_on_submit():
        f = request.files['image']
        filename = secure_filename(gen_rnd_filename() + "." + f.filename.split('.')[-1])
        if not filename:
            flash(u'请选择图片','error')
            return redirect(url_for('.home'))
        if not allowed_file(f.filename):
            flash(u'图文件名或格式错误。','error')
            return redirect(url_for('.home'))

        dataetime = dt.datetime.today().strftime('%Y%m%d')
        file_dir = 'superadmin/%s/base_products/%s/'%(current_user.id,dataetime)
        if not os.path.isdir(os.getcwd()+'/'+current_app.config['UPLOADED_PATH']+file_dir):
            os.makedirs(os.getcwd()+'/'+current_app.config['UPLOADED_PATH']+file_dir)
        f.save(current_app.config['UPLOADED_PATH'] +file_dir+filename)

        BaseProducts.create(
            title=form.title.data,
            original_price=form.original_price.data,
            special_price=form.special_price.data,
            unit=form.unit.data,
            ean=form.ean.data,
            note=form.note.data,
            category_id=form.category_id.data,            
            attach_key=form.attach_key.data,            
            attach_value=form.attach_value.data,
            main_photo = file_dir+filename,        	
        )
        flash('ok')
    return redirect(url_for('superadmin.home'))

