def areSentencesSimilar(sentence1: str, sentence2: str) -> bool:
        if len(sentence1.split()) < len(sentence2.split()):
            lst1 = sentence1.split()
            lst2 = sentence2.split()
        else:
            lst1 = sentence2.split()
            lst2 = sentence1.split()
        l1 = 0
        while l1 < len(lst1) and lst1[l1] == lst2[l1]:
            l1 += 1
        r1, r2 = len(lst1)-1, len(lst2)-1
        while r1 >= 0 and  lst1[r1] == lst2[r2]:
            r1 -= 1
            r2 -= 1
        return r1 < l1

print(areSentencesSimilar(sentence1 = "My name is Haley", sentence2 = "My Haley"))
print(areSentencesSimilar(sentence1 = "of", sentence2 = "A lot of words"))