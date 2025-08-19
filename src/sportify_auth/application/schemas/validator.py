from dataclasses import dataclass, fields
from typing import Any, Union, get_args, get_origin


@dataclass
class ValidatedDataClass:
	def __post_init__(self):
		for f in fields(self):
			value = getattr(self, f.name)
			expected_type = f.type
			self._validate_type(f.name, value, expected_type)

	def _validate_type(self, field_name: str, value: Any, expected_type: Any):
		"""Рекурсивная проверка типов"""
		origin = get_origin(expected_type)
		args = get_args(expected_type)

		# 1. Базовые типы
		if origin is None:
			if not isinstance(value, expected_type):
				raise TypeError(
					f"{field_name} must be {expected_type.__name__}, got {type(value).__name__}"
				)

		# 2. Optional / Union
		elif origin is Union:
			if value is None and type(None) in args:
				return
			if not any(self._is_instance(value, arg) for arg in args if arg is not type(None)):
				raise TypeError(f"{field_name} must be one of {args}, got {type(value).__name__}")

		# 3. Коллекции
		elif origin in (list, tuple, set):
			if not isinstance(value, origin):
				raise TypeError(
					f"{field_name} must be {origin.__name__}, got {type(value).__name__}"
				)
			if args:
				inner_type = args[0]
				for item in value:
					self._validate_type(f"{field_name}[]", item, inner_type)

		# 4. Словари
		elif origin is dict:
			if not isinstance(value, dict):
				raise TypeError(f"{field_name} must be dict, got {type(value).__name__}")
			key_type, val_type = args
			for k, v in value.items():
				self._validate_type(f"{field_name}.key", k, key_type)
				self._validate_type(f"{field_name}.value", v, val_type)

		# 5. Если встретился экзотический generic — пока игнорируем
		else:
			if not isinstance(value, expected_type):
				raise TypeError(f"{field_name} must be {expected_type}, got {type(value)}")

	def _is_instance(self, value: Any, expected_type: Any) -> bool:
		"""Вспомогательная проверка для Union"""
		try:
			return isinstance(value, expected_type)
		except TypeError:
			# для generic-типа без origin
			origin = get_origin(expected_type)
			return origin is not None and isinstance(value, origin)


# class ValidatedDataClass:
#     def __post_init__(self):
#         for f in fields(self):
#             value = getattr(self, f.name)
#             if not isinstance(value, f.type):
#                 raise TypeError(
#                     f"{f.name} must be {f.type.__name__}, got {type(value).__name__}"
#                 )
