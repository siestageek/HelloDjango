from django.http import HttpResponse
from django.shortcuts import render, redirect

from board.forms import BoardForm
from board.models import Board


def index(request):
    return render(request, 'index.html')

def list(request):
    bdlist = Board.objects.values('id','title','userid','regdate','views','thumbup')
    bdlist = bdlist.order_by('-regdate')

    bds = {'bds': bdlist}
    return render(request, 'board/list.html', bds)

def view(request, bid):
    board = Board.objects.get(id=bid)
    board.views = board.views + 1   # 조회수 증가
    board.save()
    
    bd = {'bd' : board }
    return render(request, 'board/view.html', bd)

def write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():  # 폼 내용이 잘 작성되었다면
            form.save()
            return redirect('/board/list')
    else:
        form = BoardForm()

    return render(request, 'board/write.html', {'form': form})

def update(request):
    return render(request, 'board/update.html')

def delete(request, bid):
    bd = Board.objects.get(id=bid)
    bd.delete()

    return redirect('/board/list')
