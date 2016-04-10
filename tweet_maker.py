import random
import scrape

def make_tweet(exclamations_file, adverbs_file, adjectives_file):
    
    s = scrape.Scrape()

    foodList_ldc = s.getDataLDC()[3]
    ## print(foodList_ldc)
    foodList_burt = s.getDataBurt()[3]
    ## print(foodList_burt)
    
    ex_file = open(exclamations_file)
    adv_file = open(adverbs_file)
    adj_file = open(adjectives_file)
    
    exclamations = ex_file.read().split(", ")
    adverbs = adv_file.read().split(", ")
    adjectives = adj_file.read().split(", ")
    
    food_index_ldc = random.randint(0,len(foodList_ldc)-1)
    food_index_burt = random.randint(0,len(foodList_burt)-1)
    
    ex_index_ldc = random.randint(0,len(exclamations)-1)
    ex_index_burt = random.randint(0,len(exclamations)-1)
    
    adv_index_ldc = random.randint(0,len(adverbs)-1)
    adv_index_burt = random.randint(0,len(adverbs)-1)
    
    adj_index_ldc = random.randint(0,len(adjectives)-1)
    adj_index_burt = random.randint(0,len(adjectives)-1)
    
    food_name_ldc = foodList_ldc[food_index_ldc][0].replace("\\", "")
    food_name_burt = foodList_burt[food_index_burt][0].replace("\\", "")
    
    station_name_ldc = foodList_ldc[food_index_ldc][1].replace(" ", "")
    station_name_burt = foodList_burt[food_index_burt][1].replace(" ", "")
    
    exclamation_ldc = exclamations[ex_index_ldc]
    exclamation_burt = exclamations[ex_index_burt]
    
    adverb_ldc = adverbs[adv_index_ldc]
    adverb_burt = adverbs[adv_index_burt]
    
    adjective_ldc = adjectives[adj_index_ldc]
    adjective_burt = adjectives[adj_index_burt]
    
    food_ldc = sanitize_food(food_name_ldc)
    food_burt = sanitize_food(food_name_burt)
    
    #print(food_name_ldc + " --> " + food_ldc)
    #print(food_name_burt + " --> " + food_burt)
    
    article_ldc = ""
    if food_ldc[-1] == "s":
        article_ldc = " are "
    else:
        article_ldc = " is "
        
    article_burt = ""
    if food_burt[-1] == "s":
        article_burt = " are "
    else:
        article_burt = " is "
        
    tweet_ldc = exclamation_ldc + "! I hear LDC's " + food_ldc + article_ldc + adverb_ldc + " " + adjective_ldc + ". #" + station_name_ldc + " #LDC\n"
    tweet_burt = exclamation_burt + "! I hear Burton's " + food_burt + article_burt + adverb_burt + " " + adjective_burt + ". #" + station_name_burt + " #WestSideBestSide\n"
    
    
    f = open("tweet.txt", 'w')
    f.write("Our tweet for LDC:\n")
    f.write(tweet_ldc)
    f.write("\n\nOur tweet for Burton:\n")
    f.write(tweet_burt)
    f.close
    ex_file.close()
    adv_file.close()
    adj_file.close()
    
def sanitize_food(food_name):
    words = food_name.split(" ")
    cut_index = len(words)
    for i in range(len(words)):
        print(words[i])
        if words[i].lower() == "with" or words[i].lower() == "available" or words[i].lower == "LLC\"":
            cut_index = i
        if words[i] == '{':
            words[i] = "Pasta"
#    for word in words:
#        if word == "":
#            words.remove(word)
    words = words[0:cut_index]
    finalString = ''
    for i in range(len(words)):
        if words[i] != "":
            finalString = finalString + words[i]
        if i != (len(words) - 1):
            finalString = finalString + " "
            
    #return ' '.join(words)
    return finalString

def main():
    make_tweet('exclamations.txt','adverbs.txt','adjectives.txt')
    
if __name__ == "__main__":
    main()