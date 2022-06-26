
n = [5,19,23,6,21,16,18,9,6,4,16,19,22,12,15,10,20,19,25,19]

for i in n:
    print(l[i])

# caesar
def caesar(input,output, shift):
    for i in range(26):
        pass

def alpha_number(s_in):
    l  = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    s_in = s_in

    text = ""

    for j in range(26):
        out = []

        for i in s_in:
            out.append( l[i-j] )
        
        for c in out:
            text = text + c

        text = text + "\n" 

    return text

print(alpha_number(n))