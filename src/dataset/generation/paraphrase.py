import logging

from litellm import completion

from settings import settings
from src.dataset.prompts import create_paraphrase_prompt

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def paraphrase_query(query):
    logging.info(f"Sending paraphrasing request for query: {query!r}")
    prompt = create_paraphrase_prompt(query)
    try:
        response = completion(
            model=settings.dataset.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        logging.debug(f"Received response: {response}")
        paraphrased_text = (
            response.get("choices", [{}])[0].get("message", {}).get("content")
        )
        if paraphrased_text:
            logging.info(f"Paraphrased query: {paraphrased_text.strip()!r}")
            return paraphrased_text.strip()
        else:
            logging.warning(
                f"Could not extract paraphrase from response for query: {query!r}"
            )
            return None
    except Exception as e:
        logging.error(f"Error during paraphrasing query '{query}': {e}", exc_info=True)
        return None


def paraphrase_dataset(dataset, start_id, count):
    paraphrased = []
    num_to_paraphrase = min(count, len(dataset))
    if num_to_paraphrase == 0:
        logging.info("No examples selected for paraphrasing.")
        return []

    logging.info(f"Starting paraphrasing for {num_to_paraphrase} examples.")
    for i in range(num_to_paraphrase):
        ex = dataset[i]
        logging.info(
            f"Processing example {i + 1}/{num_to_paraphrase} (id={ex.get('id', 'N/A')})"
        )
        new_query = paraphrase_query(ex["query"])
        if new_query and new_query != ex["query"]:
            logging.info(f"Original: {ex['query']!r} | Paraphrased: {new_query!r}")
            new_ex = {
                "id": start_id,
                "query": new_query,
                "answers": ex["answers"],
                "tools": ex["tools"],
            }
            paraphrased.append(new_ex)
            start_id += 1
            # Log progress periodically
            if (i + 1) % 20 == 0 or (i + 1) == num_to_paraphrase:
                logging.info(f"Paraphrased {i + 1}/{num_to_paraphrase} examples...")
        elif not new_query:
            logging.warning(
                f"Skipping example {ex.get('id', 'N/A')} due to paraphrasing error or empty result."
            )
        else:
            logging.info(
                f"Paraphrased query is identical to original for example {ex.get('id', 'N/A')}, skipping."
            )

    logging.info(f"Finished paraphrasing. Generated {len(paraphrased)} new examples.")
    return paraphrased
