from numpy import array, zeros
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

from spacq.interface.list_columns import ListParser


"""
Embeddable, generic, virtual, tabular display.
"""


class VirtualListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
	"""
	A generic virtual list.
	"""

	max_value_len = 250 # Characters.

	@staticmethod
	def find_type(value):
		"""
		Determine the type of a column based on a single value.

		The type is one of: scalar, list, string.
		"""

		try:
			float(value)
		except ValueError:
			pass
		else:
			return 'scalar'

		try:
			ListParser()(value)
		except ValueError:
			pass
		else:
			return 'list'

		return 'string'

	def __init__(self, parent, *args, **kwargs):
		wx.ListCtrl.__init__(self, parent,
				style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES,
				*args, **kwargs)

		ListCtrlAutoWidthMixin.__init__(self)

		self.reset()

	def reset(self):
		self.headings = []
		self.data = array([])
		self.display_data = array([])

		self.types = []

	def GetValue(self, types=None):
		# Get all types by default.
		if types is None:
			types = set(self.types)
		else:
			types = set(types)

		# Find column indices of the correct type.
		idxs = [i for i, t in enumerate(self.types) if t in types]

		return ([self.headings[i] for i in idxs], self.data[:,idxs], [self.types[i] for i in idxs])

	def SetValue(self, headings, data):
		"""
		headings: A list of strings.
		data: A 2D NumPy array.
		"""

		self.ClearAll()
		self.reset()

		self.headings = headings
		self.data = data

		self.ItemCount = len(data)

		if self.ItemCount > 0:
			self.display_data = zeros(self.data.shape, dtype='|S{0}'.format(self.max_value_len))

			width, height = self.GetSize()
			# Give some room for the scrollbar.
			col_width = (width - 50) / len(self.headings)

			for i, heading in enumerate(self.headings):
				self.InsertColumn(i, heading, width=col_width)

				# Truncate for display.
				self.display_data[:,i] = [x[:self.max_value_len] for x in self.data[:,i]]

				type = self.find_type(self.data[0,i])
				self.types.append(type)

		self.Refresh()

	def OnGetItemText(self, item, col):
		"""
		Return cell value for LC_VIRTUAL.
		"""

		return self.display_data[item,col]


class TabularDisplayPanel(wx.Panel):
	"""
	A panel to display arbitrary tabular data.
	"""

	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent, *args, **kwargs)

		# Panel.
		panel_box = wx.BoxSizer(wx.VERTICAL)

		## Table.
		self.table = VirtualListCtrl(self)
		panel_box.Add(self.table, proportion=1, flag=wx.EXPAND)

		self.SetSizer(panel_box)

	def __len__(self):
		return self.table.ItemCount

	def from_csv_data(self, has_header, values):
		"""
		Import the given CSV data into the table.

		If has_header is True, the first row is treated specially.
		"""

		if has_header:
			headers, rows = values[0], array(values[1:])
		else:
			headers, rows = [''] * len(values[0]), array(values)

		# Ensure that all columns have a header.
		for i, header in enumerate(headers):
			if not header:
				headers[i] = 'Column {0}'.format(i + 1)

		self.SetValue(headers, rows)

	def GetValue(self, *args, **kwargs):
		return self.table.GetValue(*args, **kwargs)

	def SetValue(self, headings, values):
		self.table.SetValue(headings, values)


class TabularDisplayFrame(wx.Frame):
	def __init__(self, parent, *args, **kwargs):
		wx.Frame.__init__(self, parent, *args, **kwargs)

		# Frame.
		frame_box = wx.BoxSizer(wx.VERTICAL)

		## Display panel.
		self.display_panel = TabularDisplayPanel(self)
		frame_box.Add(self.display_panel, proportion=1, flag=wx.EXPAND)

		self.SetSizer(frame_box)
