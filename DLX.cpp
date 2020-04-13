#include<iostream>
#include<cstdio>
#include<cstring>
#include<string>
#include<set>
#include<queue>
#include<algorithm>
#include<vector>
#include<cstdlib>
#include<cmath>
#include<ctime>
#include<stack>
#define INF 2100000000
#define ll long long
#define clr(x) memset(x,0,sizeof(x));
#define M 1000

using namespace std;

struct link2
{
    link2 *up,*down,*right,*left,*col;
    int row,count,lie;
}*head,*c[M],*link[5*M],dizhi[5*M];

int T,a[90],ans[M],sta,n;

void remove(link2 *C)
{
    C->left->right=C->right;
    C->right->left=C->left;

    link2 *i=C->down;
    while(i!=C)
    {
        link2 *j=i->right;
        while(j!=i)
        {
            j->up->down=j->down;
            j->down->up=j->up;
            j=j->right;
            j->col->count--;
        }
        i=i->down;
    }
}

void resume(link2 *C)
{
    C->left->right=C;
    C->right->left=C;

    link2 *i=C->down;
    while(i!=C)
    {
        link2 *j=i->right;
        while(j!=i)
        {
            j->up->down=j;
            j->down->up=j;
            j=j->right;
            j->col->count++;
        }
        i=i->down;
    }
}

int t;

void addline(int *index,int row)
{
    for(int i=1;i<=4;i++)
    {
        link[++t]=&dizhi[t+T];
        if(i==1)
        {
            link[t]->left=link[t];
            link[t]->right=link[t];
        }
        else
        {
            link[t]->left=link[t-1];
            link[t]->right=link[t-1]->right;
            link[t-1]->right->left=link[t];
            link[t-1]->right=link[t];
        }
        int j=index[i];
        c[j]->count++;
        link[t]->up=c[j]->up;
        c[j]->up->down=link[t];
        link[t]->down=c[j];
        c[j]->up=link[t];
        link[t]->col=c[j];
        link[t]->row=row;
        link[t]->lie=j;
    }
}

void bulid()
{
    int m=324;
    head=&dizhi[T++];
    for(int i=1;i<=m;i++)c[i]=&dizhi[T++];
    head->right=c[1];
    head->left=c[m];
    for(int i=1;i<=m;i++)
    {
        c[i]->left=i==1?head:c[i-1];
        c[i]->right=i==m?head:c[i+1];
        c[i]->up=c[i]->down=c[i];
        c[i]->count=0;
        c[i]->lie=i;
    }
    for(int i=1;i<=81;i++)
    {
        if(!a[i])continue;
        int y=(i-1)/9+1,x=(i-1)%9+1;
        int p1=i,p2=81+(y-1)*9+a[i];
        int p3=162+(x-1)*9+a[i],p4=243+((y-1)/3*3+(x-1)/3)*9+a[i];
        c[p1]->count=c[p2]->count=c[p3]->count=c[p4]->count=-1;
        c[p1]->left->right=c[p1]->right;c[p1]->right->left=c[p1]->left;
        c[p2]->left->right=c[p2]->right;c[p2]->right->left=c[p2]->left;
        c[p3]->left->right=c[p3]->right;c[p3]->right->left=c[p3]->left;
        c[p4]->left->right=c[p4]->right;c[p4]->right->left=c[p4]->left;
    }

    for(int i=1;i<=9;i++)
        for(int j=1;j<=9;j++)
            for(int k=1;k<=9;k++)
            {
                if(a[(i-1)*9+j])continue;
                int p1=(i-1)*9+j;
                int p2=81+(i-1)*9+k;
                int p3=162+(j-1)*9+k;
                int p4=243+((i-1)/3*3+(j-1)/3)*9+k;
                if(c[p1]->count==-1||c[p2]->count==-1||c[p3]->count==-1||c[p4]->count==-1)continue;
                int index[5]={0,p1,p2,p3,p4};
                addline(index,((i-1)*9+j)*10+k);
            }
}

bool dance(int x)
{
    if(head->right==head)
    {
        for(int i=1;i<=sta;i++)
            a[ans[i]/10]=ans[i]%10;
        //printf("%d:\n",n+1);
        for(int i=1;i<=81;i++)
        {
            printf("%d",a[i]);
        }

        cout<<'\n';
        return 1;
    }
    link2 *i=head->right->right;
    link2 *temp=head->right;
    while(i!=head)
    {
        if(i->count<temp->count)
            temp=i;
        i=i->right;
    }
    if(temp->down==temp)return 0;
    remove(temp);
    i=temp->down;
    while(i!=temp)
    {
        link2 *j=i->right;
        ans[++sta]=i->row;
        while(j!=i)
        {
            remove(j->col);
            j=j->right;
        }
        if(dance(x+1))return 1;
        j=i->left;
        while(j!=i)
        {
            resume(j->col);
            j=j->left;
        }
        ans[sta]=0;
        sta--;
        i=i->down;
    }
    resume(temp);
    return 0;
}

int main()
{
    cin>>n;
    while(n--)
    {
        char ch;
        getchar();
        for(int i=1;i<=81;i++)
        {
            ch=getchar();
            a[i]=ch-'0';
        }
        t=T=0;
        clr(ans);sta=0;
        clr(dizhi);clr(link);clr(c);
        bulid();
        dance(0);
    }

}