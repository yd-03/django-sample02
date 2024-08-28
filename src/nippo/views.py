from django.shortcuts import render, get_object_or_404
from .models import NippoModel
from .forms import NippoFormClass


def nippoListView(request):
    """日報の一覧を表示するビュー関数"""
    template_name = "nippo/nippo-list.html"
    ctx = {}
    # モデルの全てのオブジェクトをDBから取得
    qs = NippoModel.objects.all()
    # テンプレートに渡すコンテキストにオブジェクトリストを追加
    ctx["object_list"] = qs
    # テンプレートをレンダリングし、コンテキストを渡してHTMLを生成
    return render(request, template_name, ctx)


def nippoDetailView(request, pk):
    """特定の日報の詳細を表示するビュー関数"""
    template_name = "nippo/nippo-detail.html"
    ctx = {}
    # モデルの特定のオブジェクトをDBから取得
    # q = NippoModel.objects.get(pk=pk)
    q = get_object_or_404(NippoModel, pk=pk)
    ctx["object"] = q
    return render(request, template_name, ctx)


def nippoCreateView(request):
    """新しい日報を作成するビュー関数"""
    template_name = "nippo/nippo-form.html"
    # フォームクラスを使用してフォームを作成（初期リクエスト時は空のフォーム）
    form = NippoFormClass(request.POST or None)
    ctx = {"form": form}
    # フォームが正しいかどうかをチェック
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = NippoModel(title=title, content=content)
        obj.save()
    return render(request, template_name, ctx)


def nippoUpdateFormView(request, pk):
    """既存の日報を編集するビュー関数"""
    template_name = "nippo/nippo-form.html"
    # obj = NippoModel.objects.get(pk=pk)
    obj = get_object_or_404(NippoModel, pk=pk)
    # フォームクラスを使用してフォームを作成（初期値として、既存のオブジェクトの値をフォームにセット）
    initial_values = {"title": obj.title, "content": obj.content}
    # POSTリクエスト時はリクエストデータをフォームにセット、なければ初期値をセット
    form = NippoFormClass(request.POST or initial_values)
    ctx = {"form": form}
    ctx["object"] = obj
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
    return render(request, template_name, ctx)
