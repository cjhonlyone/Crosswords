#include <stdio.h>
#include <stdlib.h>

struct list
{
    int length;
    int array[100];
};

struct list list1;

void reverse_list(struct list *_list)
{
    int len = _list->length - 1;
    for (int i = 0; i<(_list->length >> 1) ;i++)
    {
        _list->array[i] = _list->array[i] ^ _list->array[len - i];
        _list->array[len - i] = _list->array[len - i] ^ _list->array[i];
        _list->array[i] = _list->array[i] ^ _list->array[len - i];       
    }
}
void pop_list(struct list *_list)
{
    if (_list->length == 0)
    {
        return ;
    }
    else
    {
        _list->length = _list->length - 1;
        for (int i = 0;i<_list->length;i++)
           _list->array[i] = _list->array[i+1];         
    }

}
void push_list(struct list *_list, int c)
{
     _list->length = _list->length + 1;
    for (int i = _list->length - 1;i>0;i--)
       _list->array[i] = _list->array[i-1];   

    _list->array[0] = c;   
}

void print_list(struct list *_list)
{
    for (int i = 0;i < _list->length; i++)
        printf("%d ",_list->array[i]);
    printf("\n");
}
int sum51_7[1024][8];
int sum51_4[1024][4];
int sum25_3[256][4];
void SumOfkNumber(int sum, int n, FILE* log)
{
    // 递归出口
    if (n <= 0 || sum <= 0)
        return;
    // 输出找到的结果
    if (sum == n)
    {
        // 反转list
        push_list(&list1, n);
        reverse_list(&list1);
		for (int i = 0; i < list1.length; i++)
		{
			fprintf(log, "%d", list1.array[i]);
			if (i != (list1.length-1))
				fprintf(log, ",");
		}
        fprintf(log, "\n");
        reverse_list(&list1);//此处还需反转回来
        pop_list(&list1);
    }
    push_list(&list1, n);      //典型的01背包问题
    SumOfkNumber(sum - n, n - 1, log);   //“放”n，前n-1个数“填满”sum-n
    pop_list(&list1);
    SumOfkNumber(sum, n - 1, log);     //不“放”n，n-1个数“填满”sum
}

int main()
{
	
    FILE *sumN25log;
    sumN25log = fopen("sumN25.log","w+");
    SumOfkNumber(25, 23, sumN25log);
    fclose(sumN25log);

    FILE *sumN51log;
    sumN51log = fopen("sumN51.log","w+");
    SumOfkNumber(51, 23, sumN51log);
    fclose(sumN51log);


    char linStr[32];
    char* p;
    sumN25log = fopen("sumN25.log","r");

	
    fscanf(sumN25log, "%[^\n]", linStr);
	fscanf(sumN25log, "%[^\n]", linStr);
    p = strtok(linStr, ",");
    for (int j = 0; j < 40; j++)
    {
        
        p = strtok(NULL, ",");
    }
    fclose(sumN25log);

    return 0;
}
