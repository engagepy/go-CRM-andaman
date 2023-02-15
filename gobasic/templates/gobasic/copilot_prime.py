# function for printing first 1000 prime numbers    
def prime_numbers():
    for num in range(2,1000):
        if num > 1:
            for i in range(2,num):
                if (num % i) == 0:
                    break
            else:
                print(num)          

                
                
prime_numbers()

