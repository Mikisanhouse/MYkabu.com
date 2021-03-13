from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView
from django.views import generic
from django.shortcuts import redirect
import pandas as pd
import pandas_datareader.data as web
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CodeForm
import seaborn as sns
from .models import Favorite_Code, Company_Code, BoardModel, ImageModel

# トップページのビュー


def HomePage(request):
    # 分析ツールの2つのフォーム
    context = {}
    context['form'] = CodeForm()
    return render(request, 'homepage.html', context)


# SVG化→Companyビューで使う。内容はよくわかっていない
# 参考URL：https://ebi-works.com/matplotlib-django/
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

# 企業コード入力して検索後のページ


def Company(request):
    # フォームから飛んできたとき
    if request.method == 'POST':
        # モデルの企業コードを初期化
        Company_Code.objects.all().delete()
        # コードの取得
        code = request.POST['code']
        # 企業コードをモデルへ
        Company_Code.objects.create(code=code, pk=1)
        return render(request, 'company.html', {'code': code})
    else:
        # URLがcompanyのまま。後で変更。
        return render(request, 'homepage.html', {})

# Companyページに画像を表示。


def img_plot_company(request):
    # モデルから企業コードを取ってくる
    code = Company_Code.objects.get(pk=1)
    my_date = '2020/04/01'
    my_portfolio = [code.code]
    data_source = 'yahoo'
    # 例外が発生する可能性のある文章
    try:
        # 株価取得
        ticker_data = web.DataReader(my_portfolio, data_source, my_date)
    # 例外が起こったとき
    except:
        word = 'その企業はありません。'
        return render(request, 'company.html', {'word': word})
    # 例外が起きなかった時の文章
    else:
        # Volume列削除
        ticker_data.drop('Volume', axis=1).plot()
        # SVG化。上記の関数使用。原理は不明
        svg = plt2svg()
        # グラフをリセット。
        plt.cla()
        # companyに出力。
        response = HttpResponse(svg, content_type='image/svg+xml')
        return response


def img_plot_board(request, pk):
    # モデルから企業コードを取ってくる
    code = BoardModel.objects.get(pk=pk)
    my_date = '2020/04/01'
    my_portfolio = [code.images_code]
    data_source = 'yahoo'
    # 例外が発生する可能性のある文章
    try:
        # 株価取得
        ticker_data = web.DataReader(my_portfolio, data_source, my_date)
    # 例外が起こったとき
    except:
        word = 'その企業はありません。'
        return render(request, 'company.html', {'word': word})
    # 例外が起きなかった時の文章
    else:
        # Volume列削除
        ticker_data.drop('Volume', axis=1).plot()
        # SVG化。上記の関数使用。原理は不明
        svg = plt2svg()
        # グラフをリセット。
        plt.cla()
        # companyに出力。
        response = HttpResponse(svg, content_type='image/svg+xml')
        return response

# 企業をお気に入りに入れる。


def Favorite_Create(request):
    # 検索したコードを引っ張る
    code = Company_Code.objects.get(pk=1).code
    # ログインユーザーを取得
    user = str(request.user)
    # 検索したコードをモデルに入れる
    Favorite_Code.objects.create(code=code, user=user)
    # ユーザーのお気に入りのコードを全部取り出す。
    favorite_codes = Favorite_Code.objects.all().filter(user__exact=user)
    codes_user = []
    for x in favorite_codes:
        codes_user.append(x.code)
    # 重複を無くす
    codes = list(dict.fromkeys(codes_user))
    # ユーザーのお気に入りコードを全部消す
    Favorite_Code.objects.all().filter(user__exact=user).delete()
    # もう一回入れなおす
    for favorite_code in codes:
        Favorite_Code.objects.create(code=favorite_code, user=user)
    return redirect('homepage')

# お気に入り企業の表示


@login_required
def Favorite_List(request):
    # ログインユーザーを取得
    user = str(request.user)
    object_list = Favorite_Code.objects.all().filter(user__exact=user)
    return render(request, 'favorite_list.html', {'object_list': object_list})

# お気に入りの企業のグラフを表示


def Favorite_Company(request, pk):
    # モデルをリセット
    Company_Code.objects.all().delete()
    # お気に入りの企業データを引っ張る
    object = Favorite_Code.objects.get(pk=pk)
    # データを変数に格納
    code = object.code
    # モデルに入れる。
    Company_Code.objects.create(code=code, pk=1)
    return render(request, 'company.html', {'code': code})


def Signup(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        try:
            User.objects.get(username=username2)
            return render(request, 'signup.html', {'error': 'このユーザーは登録されています'})
        except:
            user = User.objects.create_user(username2, '', password2)
            return render(request, 'signup.html', {})
    return render(request, 'signup.html', {})


def Login(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return redirect('login')
    return render(request, 'login.html', {})


def Logout(request):
    logout(request)
    return redirect('login')


def Result(request):
    if request.method == 'POST':
        # モデルを全消し
        Company_Code.objects.all().delete()
        code1 = request.POST['code1']
        code2 = request.POST['code2']
        Company_Code.objects.create(code=code1, pk=1)
        Company_Code.objects.create(code=code2, pk=2)
        return render(request, 'result.html', {})
    else:
        # URLがcompanyのまま。後で変更。
        return render(request, 'homepage.html', {})


def img_plot_reslut(request):
    # モデルから企業コードを取ってくる
    code1 = Company_Code.objects.get(pk=1)
    code2 = Company_Code.objects.get(pk=2)
    my_date = '2020/04/01'
    my_portfolio = [code1.code, code2.code]
    data_source = 'yahoo'
    try:
        # 株価取得
        ticker_data = web.DataReader(
            my_portfolio, data_source, my_date)['Adj Close']
        # 例外が起こったとき
    except:
        word = 'その企業はありません。'
        return render(request, 'result.html', {'word': word})
        # 例外が起きなかった時の文章
    else:
        tech_rets = ticker_data.pct_change()
        sns.jointplot(code1.code, code2.code, tech_rets,
                      kind='scatter', color='seagreen')
        svg = plt2svg()
        # グラフをリセット。理由は不明
        plt.cla()
        # resultに出力。
        response = HttpResponse(svg, content_type='image/svg+xml')
        return response
    return render(request, 'result.html', {})


def Board(request):
    object_list = BoardModel.objects.all()
    return render(request, 'board.html', {'object_list': object_list})


def Board_detail(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'board_detail.html', {'object': object})


class Board_create(CreateView):
    template_name = 'board_create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'images_code')
    success_url = reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # はじめに継承元のメソッドを呼び出す
        context["code"] = Company_Code.objects.get(pk=1)
        return context


class Favorite_code_delete(DeleteView):
    template_name = 'delete.html'
    model = Favorite_Code
    success_url = reverse_lazy('favorite_list')


class Board_delete(DeleteView):
    template_name = 'delete.html'
    model = BoardModel
    success_url = reverse_lazy('board')
