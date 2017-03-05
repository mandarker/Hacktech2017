import math

def print_tag_confidence(data):
    """
    Prints out the confidences of each nametag in the data set
    :param data: the data set to be working off of
    :return: void
    """
    # link = "http://img.wennermedia.com/social/trumpfamily-0a0680e3-ea21-45c5-a9ad-c51fec63dffa.jpg"
    # data = scraper.get_tag_image(link)
    for tag in data["tags"]:
        message = "This is {} with confidence {}".format(tag["name"], tag["confidence"])
        print(message)

def print_celebrity_details(data):
    """
    Prints celebrities if pictured in the dataset
    :param data: the data set to be working off of
    :return: void - print list of celebs, otherwise print that there are none
    """
    # link = "https://lh5.googleusercontent.com/-UjdvkPr9KL4/AAAAAAAAAAI/AAAAAAAAACA/WLHz8N7GHQs/photo.jpg"
    # link = "http://img.wennermedia.com/social/trumpfamily-0a0680e3-ea21-45c5-a9ad-c51fec63dffa.jpg"
    # data = scraper.get_celebrity(link)
    if not is_celebrity(data):
        print("No celebrities found")
    else:
        for person in data["result"]["celebrities"]:
            name = person["name"]
            confidence = person["confidence"]
            message = "This is {} with confidence {}".format(name, confidence)
            print(message)

def is_celebrity(data):
    """
    :param data: data set to be working off of
    :return: boolean is celeb or not
    """
    # data = scraper.get_celebrity(link)
    return len(data["result"]["celebrities"]) != 0

def calculateTagWeight(dataA, dataB):
    """
    For each nametag intersection, get a subaverage (1 - difference)
    If no intersection, set subaverage to 0
    Get total average of all of them
    :param dataA: Raw json data for one image
    :param dataB: Raw json data for another image
    :return: returns a float weight between 0 and 1
    """
    # Get the tags for both vertexes
    # We will work with the larger one compared to the smaller one to make sure we hit
    # each item
    if len(dataA) > len(dataB):
        dataLarger = dataA
        dataSmaller = dataB
    else:
        dataLarger = dataB
        dataSmaller = dataA
    subweights = []

    """
        FIX FOR EFFICIENCY LATER
    """
    for big_tag in dataLarger["tags"]:
        # if tag["name"] in dataSmaller["tags"]:
        for small_tag in dataSmaller["tags"]:
            if big_tag["name"] == small_tag["name"]:
                difference = math.fabs(big_tag["confidence"] - small_tag["confidence"])
                subweights.append(1 - difference)
                break
        else:
            subweights.append(0)
    total_tag_weight = sum(subweights) / len(subweights)
    return total_tag_weight

def calculateCelebWeight(dataA, dataB):
    """
    Calculates celebrity similarity between two images
    :param dataA: first data set to be worked off of
    :param dataB: second ata set to be worked off of
    :return: 0 if one or both images have no celebs, otherwise a normalized
        confidence based on how many matching celebs and the respective confidences
    """
    if not is_celebrity(dataA) or not is_celebrity(dataB):
        return 0
    if len(dataA) > len(dataB):
        dataLarger = dataA
        dataSmaller = dataB
    else:
        dataLarger = dataB
        dataSmaller = dataA
    subweights = []
    for big_tag in dataLarger["result"]["celebrities"]:
        for small_tag in dataSmaller["result"]["celebrities"]:
            if big_tag["result"]["celebrities"]["name"] == small_tag["result"]["celebrities"]["name"]:
                difference = math.fabs(big_tag["result"]["celebrities"]["confidence"] - small_tag["reseult"]["celebrities"]["confidence"])
                subweights.append(1 - difference)
                break
            else:
                subweights.append(0)
    total_celeb_weight = sum(subweights) / len(subweights)
    return total_celeb_weight


def calculateWordWeight(dataA, dataB):
    """
    Takes threads and gathers all their comments together to see similarities
    :param dataA: a list of comment strings
    :param dataB: another list of comment strings
    :return: float weight from 0 to 1
    """
    dictionaryA = {}
    dictionaryB = {}
    for comment in dataA:
        comment = comment.lower()
        wordList = comment.split(" ")
        for word in wordList:
            if word in dictionaryA:
                dictionaryA[word] += 1
            else:
                dictionaryA[word] = 0
    for comment in dataB:
        comment = comment.lower()
        wordList = comment.split(" ")
        for word in wordList:
            if word in dictionaryB:
                dictionaryB[word] += 1
            else:
                dictionaryB[word] = 0

    dictionaryA = sorted(dictionaryA, key=dictionaryA.get)
    dictionaryB = sorted(dictionaryB, key=dictionaryB.get)

    totalA = 0
    for item in dictionaryA:
        totalA += dictionaryA[item]
    totalB = 0
    for item in dictionaryB:
        totalB += dictionaryB[item]

    for item in dictionaryA:
        dictionaryA[item] = dictionaryA / totalA
    for item in dictionaryB:
        dictionaryB[item] = dictionaryB / totalB

    subweights = []
    if len(dictionaryA) > len(dictionaryB):
        larger = dictionaryA
        smaller = dictionaryB
    else:
        larger = dictionaryB
        smaller = dictionaryA

    for item in larger:
        if item in smaller:
            difference = math.fabs(larger[item] - smaller[item])
            subweights.append(difference)
        else:
            subweights.append(0)
    return sum(subweights) / len(subweights)