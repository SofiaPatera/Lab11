import networkx as nx

from database import dao
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._lista_rifugi = []
        self._lista_connesisoni = []
        self.idMappa = {}

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.G.clear()
        self._lista_rifugi = DAO.leggiRifugio(year)
        self.idMappa= {r.id: r for r in self._lista_rifugi}
        self.G.add_nodes_from(self._lista_rifugi) #cosi aggiungo tutti i nodi che ho gia filtrato nella query del dao
        self._lista_connesisoni = DAO.leggiConnessione(year)
        for l in self._lista_connesisoni: #archi
            r1 = self.idMappa[l.id_rifugio1]
            r2 = self.idMappa[l.id_rifugio2]
            self.G.add_edge(r1, r2)

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        return list(self.G.nodes())

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        return self.G.degree(node)

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        return nx.number_connected_components(self.G)


    def get_reachable_bfs_tree(self,start):
        tree = nx.bfs_tree(self.G, start)
        return list(tree.nodes())[1:] #tolgo il primo nodo come suggerito nel testo

    def get_reachable_recursive(self, start):
        visited = set() #mi tiene conto dei nodi che ho visditato (set cosi non si ripetono)
        def dfs(u):
            for v in self.G.neighbors(u): #guardiamo tutti i vicini di u del nodo che stiamo prendendo in consideraizone
                if v not in visited:
                    visited.add(v)
                    dfs(v) #richiamo ricorsivo per guardare anche i vicini di v
        dfs(start) #avvia la ricerca per il rifugio
        if start in visited: #se il rifugio è in quelli visitati
            visited.remove(start) #lo tolgo e mostro solo quelli che sono vicini
        return list(visited)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_recursive(start)
        return a






