# 链表中倒数第k个结点

题目描述

输入一个链表，输出该链表中倒数第k个结点。

这题的考点有两个，一个是快慢指针，一个是边界的考虑问题

快慢指针是指当需要求倒数第K个，那么可以考虑让一个快指针先走K格，如果它能够走到最后的空，那么慢指针就是对应的倒数第K个。

边界问题是，如果K为0？如果K大于了链表的长度？如果链表本身就是空？这三种情况都是需要返回空的。

所以首先让快慢指针都站在头部，先让快指针走K步，这其中如果快指针已经达到空，说明遇到了前面提到的“K大于了链表的长度”，直接返回空；如果没有，则继续走，走完K步了，两个指针就可以一起走了，直到快指针走到尾部，变成空，那么慢指针就是正确答案了。

```c++
class Solution {
public:
    ListNode* FindKthToTail(ListNode* pListHead, unsigned int k) {
        if(pListHead==nullptr || k==0) return nullptr;
        ListNode* result=pListHead;
        ListNode* faster=pListHead;
        for(int i=0;i<k;i++){
            if(faster!=nullptr){
                faster=faster->next;
            }else{
                return nullptr;
            }
        }
        while(faster){
            result=result->next;
            faster=faster->next;
        }
        return result;
    }
};
```

