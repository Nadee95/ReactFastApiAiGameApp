

export interface Option {
    node_id: string;
    text: string;
}

export interface Node {
    id: string;
    content: string;
    is_ending: boolean;
    is_winning_ending: boolean;
    options?: Option[];
}

export interface Story {
    title: string;
    root_node: Node;
    all_nodes: { [key: string]: Node };
}