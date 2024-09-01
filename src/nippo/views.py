from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
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


class NippoListView(ListView):
    """日報の一覧を表示するビュークラス"""

    template_name = "nippo/nippo-list.html"
    model = NippoModel

    def get_queryset(self):
        qs = NippoModel.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        return ctx


def nippoDetailView(request, pk):
    """特定の日報の詳細を表示するビュー関数"""
    template_name = "nippo/nippo-detail.html"
    ctx = {}
    # モデルの特定のオブジェクトをDBから取得
    # q = NippoModel.objects.get(pk=pk)
    # get_object_or_404を使うと、オブジェクトが存在しない場合は404エラーを返す
    q = get_object_or_404(NippoModel, pk=pk)
    ctx["object"] = q
    return render(request, template_name, ctx)


class NippoDetailView(DetailView):
    """特定の日報の詳細を表示するビュークラス"""

    template_name = "nippo/nippo-detail.html"
    model = NippoModel

    def get_object(self):
        return super().get_object()


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
        return redirect("nippo-list")
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
        # 送信後はリダイレクト
        if request.method == "POST":
            return redirect("nippo-list")
    return render(request, template_name, ctx)


def nippoDeleteView(request, pk):
    """既存の日報を削除するビュー関数"""
    template_name = "nippo/nippo-delete.html"
    # obj = NippoModel.objects.get(pk=pk)
    obj = get_object_or_404(NippoModel, pk=pk)
    if request.method == "POST":
        obj.delete()
    ctx = {"object": obj}
    if request.method == "POST":
        return redirect("nippo-list")
    return render(request, template_name, ctx)
