import newspaper
import sqlite3
from newspaper import Article

str_conn = 'crawl_website/Database/newspapers.db'


def get_name_category(name):
    name = name.split('/')
    name = name[-1]
    name = name.split('.')[0]
    name = name.replace('-',' ')
    return name

def crawl_category(url):
    paper = newspaper.build(url, memoize_articles=False)
    return paper

def craw_paper(url):
    paper = newspaper.build(url, memoize_articles=False)
    return paper



def get_logo(url):
    paper = Article(url, memoize_articles=False)
    paper.download()
    paper.parse()
    for img in paper.images:
        if (img.endswith('.ico') or img.endswith('.svg') or img.endswith('.png')) and 'logo' in img.lower() :
            return img
        


def insert_site(name,url,logo):
    check,_ID = check_Exit_Site(name)
    if check is True:
        return _ID
    conn = sqlite3.connect(str_conn)
    query = "INSERT INTO Site (TenWebsite,Url,Logo) VALUES (?,?,?)"
    conn.execute(query,(name,url,logo))
    conn.commit()
    id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return id

def insert_category(category,site_id):
    name = get_name_category(category)
    check, _ID = check_Exit_Category(name)
    if check is True:
        return _ID
    conn = sqlite3.connect(str_conn)
    query = "INSERT INTO DanhMuc (TenDanhMuc,Url,ID_Site) VALUES (?,?,?)"
    conn.execute(query,(name,category,site_id))
    conn.commit()
    id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return id
    


def insert_paper(title,text,authors,publish_date,top_image,url,category_id):
    conn = sqlite3.connect(str_conn)
    query = "INSERT INTO BaiViet (TieuDe,NoiDung,TacGia,NgayDang,HinhAnh,Url,ID_DanhMuc) VALUES (?,?,?,?,?,?,?)"
    conn.execute(query,(title,text,authors,publish_date,top_image,url,category_id))
    conn.commit()
    

def insert_data(namesite,url,category,num):
    site_id = insert_site(namesite,url,get_logo(url))
    for cat in category:
        category_id = insert_category(cat,site_id)
        paper = craw_paper(cat)
        if num>len(paper.articles):
            num = len(paper.articles)
        count = 0
        for article in paper.articles:
            try:
                if count == num:
                    break
                tmp = newspaper.Article(article.url,language='vi')
                tmp.download()
                tmp.parse()
                if check_Exit(str(tmp.title)):
                    continue
                insert_paper(str(tmp.title),str(tmp.text),str(tmp.authors),str(tmp.publish_date),str(tmp.top_image),str(tmp.url),category_id)
                count += 1
            except:
                print('Error: Request TimeOut !!! ',article.url)
                continue
            
            

def select_category():
    conn = sqlite3.connect(str_conn)
    query = "SELECT Site.TenWebsite,TenDanhMuc,DanhMuc.Url FROM DanhMuc,Site WHERE DanhMuc.ID_Site = Site.ID"
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def select_paper_from_category(id):
    conn = sqlite3.connect(str_conn)
    query = "SELECT * FROM BaiViet WHERE ID_DanhMuc = ?"
    data = conn.execute(query,(id,)).fetchall()
    conn.close()
    return data



def check_Exit_Site(name):
    conn = sqlite3.connect(str_conn)
    query = "SELECT * FROM Site WHERE TenWebsite = ?"
    data =  conn.execute(query,(name,)).fetchall()
    if len(data)>0:
        return True, data[0][0]
    return False, -1

def check_Exit_Category(name):
    conn = sqlite3.connect(str_conn)
    query = "SELECT * FROM DanhMuc WHERE TenDanhMuc = ?"
    data =  conn.execute(query,(name,)).fetchall()
    if len(data)>0:
        return True, data[0][0]
    return False, -1

def check_Exit(title):
    conn = sqlite3.connect(str_conn)
    query = "SELECT * FROM BaiViet WHERE TieuDe = ?"
    data =  conn.execute(query,(title,)).fetchall()
    if len(data)>0:
        return True
    return False



def select_All():
    conn = sqlite3.connect(str_conn)
    query = """SELECT BaiViet.ID,Site.TenWebsite,DanhMuc.TenDanhMuc,TieuDe,NoiDung,TacGia,NgayDang,HinhAnh,BaiViet.Url,Site.Logo,Site.ID,DanhMuc.ID
                FROM Site,DanhMuc,BaiViet 
                WHERE Site.ID = DanhMuc.ID_Site AND DanhMuc.ID = BaiViet.ID_DanhMuc"""
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def select_by_site(id):
    conn = sqlite3.connect(str_conn)
    query = """SELECT BaiViet.ID,Site.TenWebsite,DanhMuc.TenDanhMuc,TieuDe,NoiDung,TacGia,NgayDang,HinhAnh,BaiViet.Url,Site.Logo,Site.ID,DanhMuc.ID
                FROM Site,DanhMuc,BaiViet 
                WHERE Site.ID = DanhMuc.ID_Site AND DanhMuc.ID = BaiViet.ID_DanhMuc AND Site.ID = ?"""
    data = conn.execute(query,(id,)).fetchall()
    conn.close()
    return data

def select_by_category(id):
    conn = sqlite3.connect(str_conn)
    query = """SELECT BaiViet.ID,Site.TenWebsite,DanhMuc.TenDanhMuc,TieuDe,NoiDung,TacGia,NgayDang,HinhAnh,BaiViet.Url,Site.Logo,Site.ID,DanhMuc.ID
                FROM Site,DanhMuc,BaiViet 
                WHERE Site.ID = DanhMuc.ID_Site AND DanhMuc.ID = BaiViet.ID_DanhMuc AND DanhMuc.ID = ?"""
    data = conn.execute(query,(id,)).fetchall()
    conn.close()
    return data


def select_paper(id):
    conn = sqlite3.connect(str_conn)
    query = "SELECT * FROM BaiViet WHERE ID = ?"
    data = conn.execute(query,(id,)).fetchall()[0]
    conn.close()
    return data


def select_by_keyword(keyword):
    conn = sqlite3.connect(str_conn)
    query = """SELECT BaiViet.ID,Site.TenWebsite,DanhMuc.TenDanhMuc,TieuDe,NoiDung,TacGia,NgayDang,HinhAnh,BaiViet.Url,Site.Logo,Site.ID,DanhMuc.ID
                FROM Site,DanhMuc,BaiViet 
                WHERE Site.ID = DanhMuc.ID_Site AND DanhMuc.ID = BaiViet.ID_DanhMuc AND TieuDe LIKE ?"""
    data = conn.execute(query,('%'+keyword+'%',)).fetchall()
    conn.close()
    return data


def select_by_keyword_filter(keyword,category=None):
    conn = sqlite3.connect(str_conn)
    query = """SELECT BaiViet.ID,Site.TenWebsite,DanhMuc.TenDanhMuc,TieuDe,NoiDung,TacGia,NgayDang,HinhAnh,BaiViet.Url,Site.Logo,Site.ID,DanhMuc.ID
                FROM Site,DanhMuc,BaiViet 
                WHERE Site.ID = DanhMuc.ID_Site AND DanhMuc.ID = BaiViet.ID_DanhMuc AND TieuDe LIKE ? AND DanhMuc.ID = ?"""
    data = conn.execute(query,('%'+keyword+'%',category)).fetchall()
    conn.close()
    return data
    
    
def get_item_for_search_category():
    conn=sqlite3.connect(str_conn)
    query = "SELECT DanhMuc.ID,TenDanhMuc,Site.TenWebsite FROM DanhMuc,Site WHERE DanhMuc.ID_Site = Site.ID"
    data = conn.execute(query).fetchall()
    _data = []
    for d in data:
        _data.append({'ID':d[0],'TenDanhMuc':d[1],'TenWebsite':d[2]})
    return _data


def delete_paper(id):
    conn = sqlite3.connect(str_conn)
    query = "DELETE FROM BaiViet WHERE ID = ?"
    conn.execute(query,(id,))
    conn.commit()
    conn.close()