import pandas as pd
import stellargraph as sg
from stellargraph.data import EdgeSplitter
from stellargraph.mapper import GraphSAGELinkGenerator


def form_graph(edges_path, meta_path, ids_path, meta_received):
    edges = pd.read_csv(edges_path, sep=",", index_col=0)
    ID = 111180

    idss = pd.read_csv(ids_path, index_col=0, names=["paper_id"]).iloc[1:].append(
        pd.DataFrame([111180], columns=["paper_id"])).reset_index(drop=True)
    meta = pd.read_csv(meta_path, index_col=0)
    new_meta = pd.DataFrame([meta_received], columns=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    meta_final = meta.append(new_meta).reset_index(drop=True)
    meta_finall = meta_final.join(idss).set_index("paper_id")
    ids = pd.read_csv("data/cutted_edges_to.csv", index_col=0).iloc[1:].append(
        pd.DataFrame([ID], columns=["0"])).reset_index(drop=True)

    column_from = []
    for i in range(len(ids)):
        column_from.append([ID])
    column_from = pd.DataFrame(column_from, columns=["from"])
    edges_final = column_from.join(ids)
    edges_final.rename(columns={'from': '0', '0': '1'}, inplace=True)
    edges_final = edges.append(edges_final).reset_index(drop=True)
    edge_data = pd.DataFrame(
        {
            "source": list(edges_final["0"].astype(int)),
            "target": list(edges_final["1"].astype(int))
        })

    G = sg.StellarGraph(
        {"paper": meta_finall}, {"paper-cites": edge_data}
    )

    print(G.info())
    return G


def inference(embeddings):
    G = form_graph("data/cutted_edges.csv", "data/cutted_features.csv", "data/cutted_edges_to.csv", embeddings)
    edge_splitter_full = EdgeSplitter(G)

    import keras as keras
    from stellargraph.layer import MeanAggregator, LinkEmbedding
    model = keras.models.load_model('data/w_rev1.h5',
                                    custom_objects={'MeanAggregator': MeanAggregator, 'LinkEmbedding': LinkEmbedding})

    G_full, edge_ids_full, edge_labels_full = edge_splitter_full.train_test_split(
        p=0.5, method="global", keep_connected=True
    )

    batch_size = 20
    num_samples = [20, 10]

    generator = GraphSAGELinkGenerator(G, batch_size, num_samples)
    hold_out_gen = generator.flow(edge_ids_full, edge_labels_full)

    hold_out_predictions_pr = model.predict(hold_out_gen)

    ID = 111180
    EDGE_results = []
    for i in range(len(edge_ids_full)):
        if edge_ids_full[i][0] == ID or edge_ids_full[i][1] == ID:
            EDGE_results.append(i)
    predictions = [[hold_out_predictions_pr[EDGE_results[i]][0], edge_ids_full[EDGE_results[i]][0]] for i in
                   range(len(hold_out_predictions_pr[EDGE_results]))]

    a = sorted(predictions, reverse=True)[0:10]
    sorted_ids = [a[i][1] for i in range(len(a))]

    return sorted_ids
