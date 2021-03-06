#coding=utf-8

from flask import request,current_app,url_for
from flask_wechatpy import wechat_required
from wechatpy.replies import TextReply,ArticlesReply,create_reply,ImageReply

from . import blueprint
from mall.extensions import csrf_protect,wechat,db

from mall.public.models import UserOrder,Follow
from mall.store.models import Seller
from mall.user.models import User
from mall.auth.views import autoregister
from log import logger


def createmenu():
    wechat.menu.create({"button":[
        {"type":"view","name":"买买买","url":'%s'%url_for('public.home',_external=True)},\
        {"type":"view","name":"再来一单","url":'%s'%url_for('public.again',_external=True)},\

        {"type":"view","name":"我的","sub_button":[
            {
                "type":"view",
                "name":"购物车",
                "url":'%s'%url_for('user.my_buys_car',_external=True)
            },
            {
                "type":"view",
                "name":"订单",
                "url":'%s'%url_for('user.my_order',_external=True)
            },
            {
                "type":"view",
                "name":"收货地址",
                "url":'%s'%url_for('user.my_address',_external=True)
            },
        ]},\
        
    ]})


#微信获取token
@blueprint.route('/token',methods=['GET'])
@wechat_required
def token_get():
    signature = request.args.get('signature','')
    timestamp = request.args.get('timestamp','')
    nonce = request.args.get('nonce','')
    echostr = request.args.get('echostr','')
    token = current_app.config['MALL_WECHAT_TOKEN']
    sortlist = [token, timestamp, nonce]
    sortlist.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, sortlist)
    hashcode = sha1.hexdigest()
    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    return echostr



#微信token信息提交
@csrf_protect.exempt
@blueprint.route('/token',methods=['POST'])
@wechat_required
def token_post():
    msg = request.wechat_msg
    reply = ''


    if msg.type == 'text':

        event_str = msg.content[0:2]
        str_id = msg.content[2:]

        #店家显示订单详情
        if event_str == 'so':

            users_order = UserOrder.query\
                .with_entities(UserOrder,Seller,User)\
                .join(Seller,Seller.id==UserOrder.seller_id)\
                .join(User,User.id==Seller.user_id)\
                .filter(User.wechat_id==msg.source)\
                .filter(UserOrder.id==str_id)\
                .first()

            if users_order:
                redirect_url = url_for('store.show_order',id=users_order[0].id,_external=True)

                textreply_str = f'<a href="{redirect_url}">点击查看订单详情。</a>'
                
            else:
                textreply_str = '输入错误'
                

            reply = TextReply(content=textreply_str, message=msg)
            return reply


        #显示店铺地址
        if event_str == '店铺':
            redirect_url = url_for('store.home',_external=True)
            textreply_str = f'<a href="{redirect_url}">点击进入店铺主页。</a>'
            reply = TextReply(content=textreply_str, message=msg)
            return reply

        #修改用户名
        if event_str == 'un':
            user = User.query.filter_by(wechat_id=msg.source).first() 
            user.update(username=str_id)
            reply=TextReply(content='用户名已修改。', message=msg)
            return reply

        #修改密码
        if event_str == 'pd':
            user = User.query.filter_by(wechat_id=msg.source).first() 
            user.set_password(password=str_id)
            db.session.add(user)
            db.session.commit()
            reply=TextReply(content=u'密码已修改。', message=msg)
            return reply

        if event_str == '后台':
            redirect_url = url_for('superadmin.index',_external=True)
            textreply_str = f'<a href="{redirect_url}">点击进入后台主页。</a>'
            reply = TextReply(content=textreply_str, message=msg)
            return reply

    try:
        msg.event
    except Exception as e:
        logger.info(str(e))
        return TextReply(content=u'欢迎关注 隔壁小卖部', message=msg)

    #关注事件
    if msg.event == 'subscribe':
        createmenu()
        user = autoregister(msg.source)
        reply = TextReply(content=u'欢迎关注 隔壁小卖部', message=msg)
    #扫描二维码关注事件?20180510变成了scan,之前是subscribe_scan
    #scan为带场景值 subscribe_scan为普通的扫码关注
    if msg.event == 'scan' or msg.event == 'subscribe_scan':   #?
    
        createmenu()

        if msg.scene_id:

            seller = Seller.query.get_or_404(msg.scene_id)
            user = User.query.filter_by(wechat_id=msg.source).first()

            if not user:
                user = autoregister(msg.source)
            if seller.users == user:
                return TextReply(content='您不能关注自己', message=msg)
            if not Follow.query.filter_by(users=user).filter_by(seller=seller).first():
                Follow.create(
                    users = user,
                    seller = seller
                )

                seller_name = seller.name
                redirect_url = url_for('public.home',_external=True)
                textreply_str = f'您已关注{seller_name}<a href="{redirect_url}">点击进入店铺购买东西吧。</a>'
                return TextReply(content=textreply_str, message=msg)
                
            else:
                redirect_url = url_for('public.home',_external=True)
                textreply_str = f'您已关注关注过该店铺了。<a href="{redirect_url}">点击进入店铺购买东西吧。</a>'
                return  TextReply(content=textreply_str, message=msg)


        reply = TextReply(content=msg.scene_id, message=msg)


    return reply







