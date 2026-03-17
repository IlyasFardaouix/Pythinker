#!/usr/bin/env python3
"""Test creating a Qdrant collection with named vectors."""

import asyncio
import traceback

from qdrant_client import AsyncQdrantClient, models


class QdrantCollectionCreator:
    """Class for creating a Qdrant collection with named vectors."""

    def __init__(self, url: str):
        """Initialize the Qdrant client.

        Args:
            url (str): The URL of the Qdrant instance.
        """
        self.client: AsyncQdrantClient | None = None
        self.url = url

    async def create_collection(
        self,
        collection_name: str,
        vectors_config: dict,
        optimizers_config: models.OptimizersConfigDiff,
    ) -> None:
        """Create a Qdrant collection.

        Args:
            collection_name (str): The name of the collection.
            vectors_config (dict): The configuration for the vectors.
            optimizers_config (models.OptimizersConfigDiff): The configuration for the optimizers.
        """
        self.client = AsyncQdrantClient(url=self.url)
        try:
            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config,
                optimizers_config=optimizers_config,
            )
            # Check the collection info
            await self.client.get_collection(collection_name)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally:
            if self.client is not None:
                await self.client.close()


async def main():
    """Main function for testing the Qdrant collection creation."""
    url = "http://qdrant:6333"
    collection_name = "test_hybrid"
    vectors_config = {
        "dense": models.VectorParams(size=1536, distance=models.Distance.COSINE),
        "sparse": models.SparseVectorParams(),
    }
    optimizers_config = models.OptimizersConfigDiff(
        indexing_threshold=20000,
        memmap_threshold=50000,
        max_segment_size=200000,
    )

    creator = QdrantCollectionCreator(url)
    await creator.create_collection(
        collection_name=collection_name,
        vectors_config=vectors_config,
        optimizers_config=optimizers_config,
    )


if __name__ == "__main__":
    asyncio.run(main())