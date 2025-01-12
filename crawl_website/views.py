from flask import Blueprint, flash, render_template, request, redirect, url_for
from crawl_website import utils
import newspaper
from newspaper import Article

view = Blueprint('view', __name__)


category_items = utils.get_item_for_search_category()

@view.route('/', methods=['GET','POST'])
def crawl():
    data = request.form
    url = None
    print(data.get('url_website'))
    url = data.get('url_website')
    if url is not None:
        paper = utils.crawl_category(str(data.get('url_website')))
        print(paper.brand)
        tmp = []
        for category in paper.categories:
            
            print(category.url)
            tmp.append(category.url)
        return render_template('index.html',url_site=paper.url,site=paper.brand,categories=tmp)
    # url = request.form['url']
    return render_template('index.html',url=url)

@view.route('/get_papers', methods=['POST'])
def get_papers():
    data = request.form.getlist('chk_category')
    site = request.form.get('site')
    url_site = request.form.get('url_site')
    num = int(request.form.get('number_paper'))
    print(site)
    utils.insert_data(site,url_site,data,num)
    flash('Lấy bài báo thành công !!!', category='message')
    
    global category_items
    category_items = utils.get_item_for_search_category()
    return render_template('index.html',url=None, flash=flash)

@view.route('/database/<page>', methods=['GET','POST'])
def get_data(page=1):
    rows = utils.select_All()
    data = []
    for r in rows:
        strAuthors = ''
        for author in r[5]:
            strAuthors += author + ','
        data.append(
            {
                'ID': r[0],
                'TenWebsite': r[1],
                'DanhMuc': r[2],
                'TieuDe': r[3],
                'TacGia': strAuthors,
                'NgayDang': r[6],
                'HinhAnh': r[7],
                'Logo': r[9],
                'Site_ID': r[10],
                'DanhMuc_ID': r[11]
            }
        )
    page = int(page)
    per_page = 20
    start = (page-1)*per_page
    end = start + per_page
    total_pages = (len(data)+ per_page  - 1)//per_page
    items_on_page = data[start:end]
    return render_template('database.html',category_items=category_items,data=items_on_page,total_pages=total_pages,page=page)

@view.route('/database', methods=['GET','POST'])
def get_data_default(page=1):    
    rows = utils.select_All()
    data = []
    for r in rows:
        strAuthors = ''
        for author in r[5]:
            strAuthors += author + ','
        data.append(
            {
                'ID': r[0],
                'TenWebsite': r[1],
                'DanhMuc': r[2],
                'TieuDe': r[3],
                'TacGia': strAuthors,
                'NgayDang': r[6],
                'HinhAnh': r[7],
                'Logo': r[9],
                'Site_ID': r[10],
                'DanhMuc_ID': r[11]
            }
        )
    page = int(page)
    per_page = 20
    start = (page-1)*per_page
    end = start + per_page
    total_pages = (len(data)+ per_page  - 1)//per_page
    items_on_page = data[start:end]
    return render_template('database.html',category_items=category_items,data=items_on_page,total_pages=total_pages,page=page)

# data theo site
@view.route('/site_<id>/', methods=['GET'])
def get_data_site_default(id,page=1):
    rows = utils.select_by_site(id)
    data = []
    for r in rows:
        strAuthors = ''
        for author in r[5]:
            strAuthors += author + ','
        data.append(
            {
                'ID': r[0],
                'TenWebsite': r[1],
                'DanhMuc': r[2],
                'TieuDe': r[3],
                'TacGia': strAuthors,
                'NgayDang': r[6],
                'HinhAnh': r[7],
                'Logo': r[9],
                'Site_ID': r[10],
                'DanhMuc_ID': r[11]
            }
        )
    page = int(page)
    per_page = 20
    start = (page-1)*per_page
    end = start + per_page
    total_pages = (len(data)+ per_page  - 1)//per_page
    items_on_page = data[start:end]    
    return render_template('site.html',category_items=category_items,id_site=id,data=items_on_page,total_pages=total_pages,page=page)

# data theo danh muc
@view.route('/danhmuc_<id>/', methods=['GET'])
def get_data_category_default(id,page=1):
    rows = utils.select_by_category(id)
    data = []
    for r in rows:
        strAuthors = ''
        for author in r[5]:
            strAuthors += author + ','
        data.append(
            {
                'ID': r[0],
                'TenWebsite': r[1],
                'DanhMuc': r[2],
                'TieuDe': r[3],
                'TacGia': strAuthors,
                'NgayDang': r[6],
                'HinhAnh': r[7],
                'Logo': r[9],
                'Site_ID': r[10],
                'DanhMuc_ID': r[11]
            }
        )   
    page = int(page)
    # page = request.args.get('page',1,type=int)
    per_page = 20
    start = (page-1)*per_page
    end = start + per_page
    total_pages = (len(data)+ per_page  - 1)//per_page
    items_on_page = data[start:end]    
    return render_template('category.html',category_items=category_items,id_cat=id,data=items_on_page,total_pages=total_pages,page=page)

# data theo site - trang
@view.route('/site_<id>/<page>', methods=['GET'])
def get_data_site(id,page=1):
    rows = utils.select_by_site(id)
    data = []
    for r in rows:
        strAuthors = ''
        for author in r[5]:
            strAuthors += author + ','
        data.append(
            {
                'ID': r[0],
                'TenWebsite': r[1],
                'DanhMuc': r[2],
                'TieuDe': r[3],
                'TacGia': strAuthors,
                'NgayDang': r[6],
                'HinhAnh': r[7],
                'Logo': r[9],
                'Site_ID': r[10],
                'DanhMuc_ID': r[11]
            }
        )
    page = int(page)
    # page = request.args.get('page',1,type=int)
    per_page = 20
    start = (page-1)*per_page
    end = start + per_page
    total_pages = (len(data)+ per_page  - 1)//per_page
    items_on_page = data[start:end]    
    return render_template('site.html',category_items=category_items,id_site=id,data=items_on_page,total_pages=total_pages,page=page)

# data theo danh muc - trang
@view.route('/danhmuc_<id>/<page>', methods=['GET'])
def get_data_category(id,page=1):
    rows = utils.select_by_category(id)
    data = []
    for r in rows:
        strAuthors = ''
        for author in r[5]:
            strAuthors += author + ','
        data.append(
            {
                'ID': r[0],
                'TenWebsite': r[1],
                'DanhMuc': r[2],
                'TieuDe': r[3],
                'TacGia': strAuthors,
                'NgayDang': r[6],
                'HinhAnh': r[7],
                'Logo': r[9],
                'Site_ID': r[10],
                'DanhMuc_ID': r[11]
            }
        )
    page = int(page)
    # page = request.args.get('page',1,type=int)
    per_page = 20
    start = (page-1)*per_page
    end = start + per_page
    total_pages = (len(data)+ per_page  - 1)//per_page
    items_on_page = data[start:end]    
    return render_template('category.html',category_items=category_items,id_cat=id,data=items_on_page,total_pages=total_pages,page=page)

@view.route('/paper/<id>', methods=['GET'])
def get_paper(id):
    row = utils.select_paper(id)
    _data = {
        'ID': row[0],
        'TieuDe': row[1],
        'NoiDung': row[2],
        'TacGia': row[3],
        'NgayDang': row[4],
        'HinhAnh': row[5],
        'Url': row[6]
    }
    print(row[1])
    return render_template('paper.html',data=_data)

@view.route('/search', methods=['POST'])
def search_keyword():
    data = request.form
    keyword = data.get('keyword')
    category = data.get('select_cat')
    if category == '0':
        if keyword == '':
            rows = utils.select_All()
        else:
            rows = utils.select_by_keyword(keyword)
    else:
        if keyword == '':
            rows = utils.select_by_category(category)
        else:
            rows = utils.select_by_keyword_filter(keyword,category)
    data = []
    for r in rows:
        strAuthors = ''
        for author in r[5]:
            strAuthors += author + ','
        data.append(
            {
                'ID': r[0],
                'TenWebsite': r[1],
                'DanhMuc': r[2],
                'TieuDe': r[3],
                'TacGia': strAuthors,
                'NgayDang': r[6],
                'HinhAnh': r[7],
                'Logo': r[9],
                'Site_ID': r[10],
                'DanhMuc_ID': r[11]
            }
        )
    return render_template('search.html',id_cat_filter=int(category),keyword=keyword,category_items=category_items,data=data)

@view.route('/delete', methods=['POST'])
def delete():
    id = request.form.get('id')
    utils.delete_paper(id)
    flash('Xóa bài báo thành công !!!', category='message')
    return redirect(url_for('view.get_data_default'))
    