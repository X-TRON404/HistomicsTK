import json
from pathlib import Path

import histomicstk
from histomicstk.cli import utils
from histomicstk.cli.utils import CLIArgumentParser
from histomicstk.preprocessing.color_normalization import background_intensity


def main(args):
    other_args = {'outputAnnotationFile', 'scheduler'}
    kwargs = {k: v for k, v in vars(args).items()
              if k not in other_args}
    # Allow (some) default parameters to work.  Assume certain values
    # are not valid.
    for k in 'sample_fraction', 'sample_approximate_total':
        if kwargs[k] == -1:
            del kwargs[k]

    utils.create_dask_client(args)
    I_0 = background_intensity(**kwargs)

    #
    # Write annotation file
    #

    print('\n>> Writing annotation file ...\n')

    annotation = {
        'name': 'BackgroundIntensity',
        'attributes': {
            'intensity_values': I_0.tolist(),
            'params': vars(args),
            'cli': Path(__file__).stem,
            'version': histomicstk.__version__,
        },
    }

    with open(args.outputAnnotationFile, 'w') as annotation_file:
        json.dump(annotation, annotation_file, separators=(',', ':'), sort_keys=False)


if __name__ == '__main__':
    main(CLIArgumentParser().parse_args())
