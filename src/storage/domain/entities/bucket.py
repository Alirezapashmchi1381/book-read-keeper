from dataclasses import dataclass, field
from typing import Optional
from src.storage.domain.entities.object import Object 
from src.storage.domain.value_objects.bucket_id import BucketID
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass

@dataclass
class Bucket:
    _id: BucketID             
    _owner: str
    _max_objects: int = 1000
    _size: int
    _size_used: int = field(default=0, init=False)
    _object_count: int = field(default=0, init=False)
    

    def create_object(self, key: ObjectKey, content_type: str,
                      storage_class: StorageClass, size: int) -> "Object":  
        if self._object_count >= self._max_objects:
            raise RuntimeError(f"Bucket {self._id.name} has reached max object limit")
        if self._size_used >= self._size:
                    raise RuntimeError(f"Bucket {self._id.name} has reached max object limit")
                
        
        self._size_used += size
        self._object_count += 1
        
        return Object.create(
            bucket_id=self._id,
            key=key,
            content_type=content_type,
            storage_class=storage_class,
            size= size
        )
    
    @classmethod
    def create(
        cls,
        bucket_id: BucketID,
        owner: str,
        size : int,
        max_objects: int = 1000,
    ) -> "Bucket":
        if not owner or not owner.strip():
            raise ValueError("Owner must be a non-empty string")
        if max_objects <= 0:
            raise ValueError("max_objects must be greater than 0")
        if size <= 0:
            raise ValueError("size must be greater than 0")

        return cls(
            bucket_id=bucket_id,
            owner=owner.strip(),
            max_objects=max_objects,
            size= size,
            object_count=0,
        )