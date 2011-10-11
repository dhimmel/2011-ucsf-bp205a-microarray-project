import os, sys
import re, copy, cPickle

class DataSet(object):

    # Constructor {{{1

    # The constructor for this class is not meant to be called directly!  To
    # create a new data set object from a GenePix results file, use the
    # DataSet.load() method.  To create a data set from previously saved data,
    # use the DataSet.restore() method.

    def __init__(self, path, attributes, features):
        self.path = path
        self.features = features

        self.type = attributes["Type"]
        self.date_time = attributes["DateTime"]
        self.settings = attributes["Settings"]

        self.array_list_file = attributes["GalFile"]
        self.image_files = attributes["ImageFiles"]
        self.jpeg_image = attributes["JpegImage"]
        self.image_origin = attributes["ImageOrigin"]
        self.jpeg_origin = attributes["JpegOrigin"]

        self.pixel_size = attributes["PixelSize"]
        self.wavelengths = attributes["Wavelengths"]
        self.normalization_method = attributes["NormalizationMethod"]
        self.normalization_factors = attributes["NormalizationFactors"]
        self.stddev = attributes["StdDev"]
        self.ratio_formulations = attributes["RatioFormulations"]
        self.feature_type = attributes["FeatureType"]
        self.background_subtraction = attributes["BackgroundSubtraction"]

        self.focus_position = attributes["FocusPosition"]
        self.temperature = attributes["Temperature"]
        self.lines_averaged = attributes["LinesAveraged"]
        self.pmt_gain = attributes["PMTGain"]
        self.scan_power = attributes["ScanPower"]
        self.laser_power = attributes["LaserPower"]
        self.filters = attributes["Filters"]
        self.scan_region = attributes["ScanRegion"]

        self.creator = attributes["Creator"]
        self.scanner = attributes["Scanner"]
        self.supplier = attributes["Supplier"]
        self.barcode = attributes["Barcode"]
        self.comment = attributes["Comment"]

    # }}}1

    # Iteration Operator {{{1
    def __iter__(self):
        for feature in self.features:
            yield feature

    # Length Operator {{{1
    def __len__(self):
        return len(self.features)

    # }}}1

    # Load {{{1
    @staticmethod
    def load(path):

        # This method reads in data from the specified GenePix results file. 
        # In order to prevent confusing mistakes, the given path must have the
        # GPR extension.

        extension = os.path.splitext(path)[1][1:].upper()
        assert extension == 'GPR', \
                "The argument passed to load() must be a GPR file path."

        # These regular expressions are rather dense, but they match the three
        # types of lines found in GenePix results files.  The feature pattern
        # will also match the header line, so it is important to check the
        # header pattern first.

        attribute_pattern = re.compile(r'"(\w*)=([^"]*)"')
        header_pattern = re.compile(r'\s+'.join(56 * ['"([^="]*)"']))
        feature_pattern = re.compile(r'\s+'.join(56 * ['(\S*)']))

        # All of the values in the GenePix results file will be read in as
        # strings by default.  This function is used to convert these raw
        # values into more useful data types.

        def cast(column, value):
            string_columns = 'Name', 'ID'
            float_columns = (
                    'Ratio of Medians (635/532)', 'Ratio of Means (635/532)',
                    'Median of Ratios (635/532)', 'Mean of Ratios (635/532)',
                    'Ratios SD (635/532)', 'Rgn Ratio (635/532)',
                    'Rgn R2 (635/532)', 'Log Ratio (635/532)',
                    'SNR 635', 'SNR 532' )

            if column in string_columns:
                return str(value.strip('"'))

            elif column in float_columns:
                if value == 'Error': value = 'NaN'
                return float(value)

            else:
                return int(value)

        attributes = {}
        features = []

        with open(path) as file:
            for line in file:

                attribute_match = attribute_pattern.match(line)
                header_match = header_pattern.match(line)
                feature_match = feature_pattern.match(line)

                if attribute_match:
                    name, value = attribute_match.groups()
                    attributes[name] = value

                elif header_match:
                    header = header_match.groups()

                elif feature_match:
                    values = line.replace('"', '').split()
                    properties = {
                            key : cast(key, value)
                            for key, value in zip(header, values) }

                    feature = Feature(properties)
                    features.append(feature)

                else:
                    pass

        return DataSet(path, attributes, features)

    # Restore {{{1
    @staticmethod
    def restore(path):

        # Data sets are stored as python pickles.  The usual file extension for
        # pickle data is PKL, and that convention is enforced by this method to
        # avoid confusion.

        extension = os.path.splitext(path)[1][1:].upper()
        assert extension == 'PKL', \
                "The argument passed to restore() must be a PKL file path."

        with open(path) as file:
            data_set = cPickle.load(file)

            # Make sure the restored object is actually a DataSet.  If some
            # different type of object is unpickled, it could cause really
            # strange bugs.

            assert isinstance(data_set, DataSet)
            return data_set

    # Save {{{1
    def save(self, path):

        # Data sets are stored as python pickles.  The usual file extension for
        # pickle data is PKL, and that convention is enforced by this method to
        # avoid confusion.

        extension = os.path.splitext(path)[1][1:].upper()
        assert extension == 'PKL', \
                "The argument passed to save() must be a PKL file path."

        with open(path, 'w') as file:
            cPickle.dump(self, file)

    # }}}1

    # Sort {{{1
    def sort(self, key, reverse=False):
        self.features.sort(key=key, reverse=(not reverse))

    # Apply {{{1
    def apply(self, function):
        self.features = map(function, self.features)

    # Prune {{{1
    def prune(self, criterion):
        self.features = [
                feature for feature in self.features
                if not criterion(feature) ]

    # Retain {{{1
    def retain(self, criterion):
        self.features = [
                feature for feature in self.features
                if criterion(feature) ]

    # Select {{{1
    def select(self, index, default=None):
        try:
            return self.features[index]
        except IndexError:
            return default

    # Truncate {{{1
    def truncate(self, features):
        self.features = self.features[0:features]

    # }}}1
    
    #Search {{{1
    def search(self, criterion):
        return [feature for feature in self.features if criterion(feature)]


    # Display {{{1
    def display(self, feature_template, header_template=""):
        if header_template:
            print header_template.format(self)

        for feature in self:
            print feature_template.format(feature)

    # Tabulate {{{1
    @staticmethod
    def tabulate(header_template, feature_template, *sets):
        
        from sys import stdout

        for data in sets:
            display = header_template.format(data)
            stdout.write("{0:<50}".format(display))

        stdout.write('\n')

        lengths = map(len, sets)
        longest = max(lengths)

        for index in range(longest):
            for data in sets:
                feature = data.select(index)
                display = feature_template.format(feature) if feature else ""
                stdout.write("{0:<50}".format(display))

            stdout.write('\n')

    # }}}1

class Feature:

    # Constructor {{{1
    def __init__(self, parameters):

        self.signal = FeatureData()
        self.signal.red = FeatureData()
        self.signal.green = FeatureData()
        
        self.s = self.signal
        self.s.r = self.signal.red
        self.s.g = self.signal.green

        self.background = FeatureData()
        self.background.red = FeatureData()
        self.background.green = FeatureData()
        
        self.b = self.background
        self.b.r = self.background.red
        self.b.g = self.background.green

        # Generic Attributes {{{2
        self.block = parameters['Block']
        self.column = parameters['Column']
        self.row = parameters['Row']
        self.position = self.block, self.row, self.column
        self.name = parameters['Name']
        self.id = parameters['ID']
        self.x = parameters['X']
        self.y = parameters['Y']
        self.diameter = parameters['Dia.']
        self.circularity = parameters['Circularity']

        self.ratio_of_medians = parameters['Ratio of Medians (635/532)']
        self.ratio_of_means = parameters['Ratio of Means (635/532)']
        self.median_of_ratios = parameters['Median of Ratios (635/532)']
        self.mean_of_ratios = parameters['Mean of Ratios (635/532)']
        self.sum_of_medians = parameters['Sum of Medians (635/532)']
        self.sum_of_means = parameters['Sum of Means (635/532)']
        self.log_ratio = parameters['Log Ratio (635/532)']
        self.ratios_stddev = parameters['Ratios SD (635/532)']
        self.regression_ratio = parameters['Rgn Ratio (635/532)']
        self.regression_quality = parameters['Rgn R2 (635/532)']

        self.flags = parameters['Flags']
        self.normalize = parameters['Normalize']
        self.autoflag = parameters['Autoflag']

        # }}}2

        # Signal Attributes {{{2
        self.signal.pixels = parameters['F Pixels']

        self.signal.red.median = parameters['F635 Median']
        self.signal.red.mean = parameters['F635 Mean']
        self.signal.red.stddev = parameters['F635 SD']
        self.signal.red.variation = parameters['F635 CV']
        self.signal.red.corrected_median = parameters['F635 Median - B635']
        self.signal.red.corrected_mean = parameters['F635 Mean - B635']

        self.signal.red.intensity = parameters['F635 Total Intensity']
        self.signal.red.signal_to_noise = parameters['SNR 635']
        self.signal.red.percent_brighter = parameters['% > B635+1SD']
        self.signal.red.percent_much_brighter = parameters['% > B635+2SD']
        self.signal.red.percent_saturated = parameters['F635 % Sat.']

        self.signal.green.median = parameters['F532 Median']
        self.signal.green.mean = parameters['F532 Mean']
        self.signal.green.stddev = parameters['F532 SD']
        self.signal.green.variation = parameters['F532 CV']
        self.signal.green.corrected_median = parameters['F532 Median - B532']
        self.signal.green.corrected_mean = parameters['F532 Mean - B532']

        self.signal.green.intensity = parameters['F532 Total Intensity']
        self.signal.green.signal_to_noise = parameters['SNR 532']
        self.signal.green.percent_brighter = parameters['% > B532+1SD']
        self.signal.green.percent_much_brighter = parameters['% > B532+2SD']
        self.signal.green.percent_saturated = parameters['F532 % Sat.']

        # Background Attributes {{{2
        self.background.pixels = parameters['B Pixels']

        self.background.red.median = parameters['B635 Median']
        self.background.red.mean = parameters['B635 Mean']
        self.background.red.stddev = parameters['B635 SD']
        self.background.red.variation = parameters['B635 CV']

        self.background.green.median = parameters['B532 Median']
        self.background.green.mean = parameters['B532 Mean']
        self.background.green.stddev = parameters['B532 SD']
        self.background.green.variation = parameters['B532 CV']

    # }}}1

    # Equality Operator {{{1
    def __eq__(self, other):
        return self.id == other.id

    # Hashing Operator {{{1
    def __hash__(self):
        return hash(self.id)

    # }}}1

class FeatureData:
    pass

