from Vertex import Graph
import scraper, weight, tester

def main():
    # Fill this from Spring / Michael code - getting from Reddit
    # { "url" : [comments] }
    content = tester.get_urls()
    # To be filled with data from MS Vision API
    dataList = []
    metadata = {}
    imageGraph = Graph()
    # Add MS Vision data to dataList
    for url in content.keys():
        metadata[url] = {
            "comments": content[url],
            "tag": scraper.get_tag_image(url),
            "celeb": scraper.get_celebrity(url)
        }
        imageGraph.add_vertex(url)
        """dataList.append({
            "url" : url,
            "comments" : content[url],
            "tag" : scraper.get_tag_image(url),
            "celeb" : scraper.get_celebrity(url)
        })"""
    print("something")
    # Instantiate image graph

    # Add necessary data points from dataList to the imageGraph
    # Create edges between EVERYTHING
    for vertex in imageGraph:
        for othertex in imageGraph:
            # If there is not already an edge, add it
            if othertex not in vertex:
                vert_data = metadata[vertex.data]
                othertex_data = metadata[othertex.data]
                cost = weight.calculate_total_image_weight(
                    vert_data["tag"], othertex_data["tag"],
                    vert_data["celeb"], othertex_data["celeb"]
                )
                if cost > 0:
                    imageGraph.add_edge(vertex, othertex, cost)

    # Create a wordGraph
    wordGraph = Graph()
    # Add comments from dataList to this graph
    for url in metadata.keys():
        wordGraph.add_vertex(url)
        # wordGraph.add_vertex({
        #     data["url"],
        #     data["comments"]
        # })
    # Create edges between EVERYTHING
    for vertex in wordGraph:
        for othertex in wordGraph:
            # If there is not already an edge, add it
            if othertex not in vertex:
                vert_data = metadata[vertex.data]
                othertex_data = metadata[othertex.data]
                cost = weight.calculate_word_weight(
                    vert_data["comments"], othertex_data["comments"]
                )
                if cost > 0:
                    wordGraph.add_edge(vertex, othertex, cost)

    print("Weights for imageGraph")
    printWeights(imageGraph)
    print("\n\n===================\n\n")
    printWeights(wordGraph)

def printWeights(graph):
    for vertex in graph:
        neighbors = vertex.get_connections()
        for neighbor in neighbors:
            print(vertex["url"] + " to " + neighbor["url"] + " weight is " + vertex.get_weight(neighbor))

main()