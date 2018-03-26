#coding=utf-8

from mall.database import Column, Model, SurrogatePK, db, reference_col, relationship

import datetime as dt

#用户收货地址
class UserAddress(SurrogatePK, Model):

	__tablename__ = 'user_address'

	user_id = reference_col('users')

	#姓名
	name = Column(db.String(20)) 
	#地址
	address = Column(db.String(255)) 
	#电话
	phone = Column(db.String(20)) 
	#状态  0为默认收货地址  默认为1
	state = Column(db.Integer(),default=1)

	user_order_id = relationship('UserOrder', backref='users_address')
    


#用户购物车商品列表
class BuysCar(SurrogatePK, Model):

	__tablename__ = 'buys_car'

	user_id = reference_col('users')
	goods_id = reference_col('goodsed')

	count = Column(db.Integer,default=1)



#用户订单
class UserOrder(SurrogatePK,Model):

	__tablename__ = 'user_order'

	#购买者
	user_id = reference_col('users')
	#收货人地址
	receive = reference_col('user_address')

	#卖家
	seller_id = reference_col('sellers')

	#订单号
	number = db.Column(db.String(100),unique=True) 
	#下单时间
	buy_time = Column(db.DateTime,default=dt.datetime.now)
    
	#发货时间
	send_time =  db.Column(db.DateTime) 
	#配送费
	freight = db.Column(db.Numeric(15,2),default=0)

	#优惠金额
	discount = db.Column(db.Numeric(15,2))
	#支付金额
	pay_price = db.Column(db.Numeric(15,2))
	#支付时间
	pay_time =  db.Column(db.DateTime) 

	#积分
	integral = db.Column(db.Integer())
	#备注
	note = db.Column(db.String(255)) 

	#买家是否评价
	evaluate_buyers = Column(db.Boolean(),default=False)
	#买家评价时间
	evaluate_buyers_time = db.Column(db.DateTime) 
	#评价内容
	evaluate_buyers_note = db.Column(db.UnicodeText())

	#卖家是否评价
	evaluate_seller = Column(db.Boolean(),default=False)
	#评价时间
	evaluate_seller_time = db.Column(db.DateTime) 
	#评价内容
	evaluate_seller_note = db.Column(db.UnicodeText())
	
	#状态默认0
	order_state = db.Column(db.Integer(),default=0)

	#出售的商品
	sale_id = relationship('Sale', backref='user_order')
    


#用户关注的店铺
class Follow(SurrogatePK,Model):
	__tablename__ = 'follows'

	user_id = reference_col('users')
	seller_id = reference_col('sellers')
	
	timestamp = db.Column(db.DateTime, default=dt.datetime.utcnow)


