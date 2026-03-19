from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Tuple

Interaction = Tuple[str, str, str]
SummaryV1Row = Dict[str, object]
SummaryV2Row = Dict[str, object]


def validate_interaction(interaction: Sequence[str]) -> Interaction:
    """
    Validate a single interaction and return it as a normalized tuple.

    Expected format:
        (TF, gene, effect)

    Rules:
    - interaction must have exactly 3 elements
    - effect must be '+' or '-'
    - TF and gene must be non-empty strings
    """
    if len(interaction) != 3:
        raise ValueError(
            f"Invalid interaction {interaction!r}: expected exactly 3 elements "
            "(TF, gene, effect)."
        )

    tf, gene, effect = interaction

    if not isinstance(tf, str) or not tf.strip():
        raise ValueError(f"Invalid TF in interaction {interaction!r}.")

    if not isinstance(gene, str) or not gene.strip():
        raise ValueError(f"Invalid gene in interaction {interaction!r}.")

    if effect not in {"+", "-"}:
        raise ValueError(
            f"Invalid effect {effect!r} in interaction {interaction!r}: "
            "expected '+' or '-'."
        )

    return tf.strip(), gene.strip(), effect


def validate_interactions(
    interactions: Iterable[Sequence[str]],
) -> List[Interaction]:
    """
    Validate all interactions and return a clean list of Interaction tuples.
    """
    return [validate_interaction(interaction) for interaction in interactions]


def deduplicate_exact_interactions(
    interactions: Iterable[Interaction],
) -> List[Interaction]:
    """
    Remove only exact duplicate interactions, preserving first appearance order.

    Example:
        ('AraC', 'araA', '+')
        ('AraC', 'araA', '+')   -> second one removed

    But:
        ('AraC', 'araA', '+')
        ('AraC', 'araA', '-')   -> both are kept
    """
    seen = set()
    unique_interactions: List[Interaction] = []

    for interaction in interactions:
        if interaction not in seen:
            seen.add(interaction)
            unique_interactions.append(interaction)

    return unique_interactions


def classify_tf(num_activated: int, num_repressed: int) -> str:
    """
    Classify a TF according to the presence of activation and repression.

    Rules:
    - activador: only '+'
    - represor: only '-'
    - dual: both '+' and '-'
    """
    if num_activated > 0 and num_repressed > 0:
        return "dual"
    if num_activated > 0 and num_repressed == 0:
        return "activador"
    if num_repressed > 0 and num_activated == 0:
        return "represor"

    raise ValueError(
        "Cannot classify TF with zero activated genes and zero repressed genes."
    )


def build_summary_v1(interactions: Iterable[Sequence[str]]) -> List[SummaryV1Row]:
    """
    Build summary version 1.

    Output fields per TF:
    - tf
    - total
    - genes

    'total' counts unique genes per TF.
    'genes' is an alphabetically sorted list of unique genes.
    """
    validated = validate_interactions(interactions)
    unique_interactions = deduplicate_exact_interactions(validated)

    regulon: Dict[str, set[str]] = {}

    for tf, gene, _effect in unique_interactions:
        if tf not in regulon:
            regulon[tf] = set()
        regulon[tf].add(gene)

    rows: List[SummaryV1Row] = []
    for tf in sorted(regulon):
        genes = sorted(regulon[tf])
        rows.append(
            {
                "tf": tf,
                "total": len(genes),
                "genes": genes,
            }
        )

    return rows


def build_summary_v2(interactions: Iterable[Sequence[str]]) -> List[SummaryV2Row]:
    """
    Build summary version 2.

    Output fields per TF:
    - tf
    - total
    - activated
    - repressed
    - type

    Notes:
    - exact duplicate interactions are removed
    - total counts unique genes regulated by the TF
    - activated counts unique genes with '+'
    - repressed counts unique genes with '-'
    - a gene can contribute to both activated and repressed if it appears
      with both signs for the same TF
    """
    validated = validate_interactions(interactions)
    unique_interactions = deduplicate_exact_interactions(validated)

    summary: Dict[str, Dict[str, set[str]]] = {}

    for tf, gene, effect in unique_interactions:
        if tf not in summary:
            summary[tf] = {
                "all_genes": set(),
                "activated_genes": set(),
                "repressed_genes": set(),
            }

        summary[tf]["all_genes"].add(gene)

        if effect == "+":
            summary[tf]["activated_genes"].add(gene)
        elif effect == "-":
            summary[tf]["repressed_genes"].add(gene)

    rows: List[SummaryV2Row] = []
    for tf in sorted(summary):
        total = len(summary[tf]["all_genes"])
        activated = len(summary[tf]["activated_genes"])
        repressed = len(summary[tf]["repressed_genes"])
        tf_type = classify_tf(activated, repressed)

        rows.append(
            {
                "tf": tf,
                "total": total,
                "activated": activated,
                "repressed": repressed,
                "type": tf_type,
            }
        )

    return rows


def format_summary_v1(rows: List[SummaryV1Row]) -> str:
    """
    Format version 1 summary as a plain text table.
    """
    if not rows:
        return "No data."

    headers = ("TF", "Total", "Genes")
    body = []

    for row in rows:
        genes_str = ", ".join(row["genes"])
        body.append((str(row["tf"]), str(row["total"]), genes_str))

    widths = [
        max(len(headers[i]), max(len(record[i]) for record in body))
        for i in range(len(headers))
    ]

    lines = []
    header_line = " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
    separator = "-+-".join("-" * widths[i] for i in range(len(headers)))
    lines.append(header_line)
    lines.append(separator)

    for record in body:
        lines.append(
            " | ".join(record[i].ljust(widths[i]) for i in range(len(record)))
        )

    return "\n".join(lines)


def format_summary_v2(rows: List[SummaryV2Row]) -> str:
    """
    Format version 2 summary as a plain text table.
    """
    if not rows:
        return "No data."

    headers = ("TF", "Total", "Activados", "Reprimidos", "Tipo")
    body = []

    for row in rows:
        body.append(
            (
                str(row["tf"]),
                str(row["total"]),
                str(row["activated"]),
                str(row["repressed"]),
                str(row["type"]),
            )
        )

    widths = [
        max(len(headers[i]), max(len(record[i]) for record in body))
        for i in range(len(headers))
    ]

    lines = []
    header_line = " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
    separator = "-+-".join("-" * widths[i] for i in range(len(headers)))
    lines.append(header_line)
    lines.append(separator)

    for record in body:
        lines.append(
            " | ".join(record[i].ljust(widths[i]) for i in range(len(record)))
        )

    return "\n".join(lines)


def main() -> None:
    """
    Demo run for the exercise.
    (+) extended version added
    (+) raw data import
    """
    filename = "data/raw/NetworkRegulatorGene.tsv"

    interactions = List()

    with open(filename) as f:
        for line in f:
            line = line.strip()

            #ignore empty lines
            if not line:
                continue

            #ignore comment lines
            if line.startswith("#"):
                continue

            #ignore heading
            if line.startswith("1)regulatorId"):
                continue

            field = line.split("\t")

            #Validate min column number
            if len(field) <= 6:
                continue

            TF = field(1)
            gene = field(4)
            effect = field(5)

    interactions.append((TF, gene, effect))

    summary_v1 = build_summary_v1(interactions)
    summary_v2 = build_summary_v2(interactions)

    print("=== Resumen versión 1 ===")
    print(format_summary_v1(summary_v1))
    print()

    print("=== Resumen versión 2 ===")
    print(format_summary_v2(summary_v2))


if __name__ == "__main__":
    main()