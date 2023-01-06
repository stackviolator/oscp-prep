var sillydate = 0;
var sillyvar = 0;

function StringArray(_length) {
    this['length'] = _length;
    for (var _count = 1; _count <= _length; _count++) {
        this[_count] = ' ';
    };
};
image = new StringArray(10);
image[0] = 'offsecphun1.gif';
image[1] = 'offsecphun2.png';
image[2] = 'offsecphun1.gif';
image[3] = 'offsecphun2.png';
image[4] = 'offsecphun1.gif';
image[5] = 'offsecphun2.png';
image[6] = 'offsecphun1.gif'
image[7] = 'offsecphun2.png';
image[8] = 'offsecphun2.png';
image[9] = 'offsecphun2.png';
var ran = 60 / image['length'];

function _create_path() {
    sillydate = new Date();
    sillyvar = sillydate['getSeconds']();
    sillyvar = Math['floor'](sillyvar / ran);
    return (image[sillyvar]);
};

function _img_create(_path) {
    var hmmmm = document.createElement("img");
    hmmmm.src = "/" + _path;
    document.body.appendChild(hmmmm);
}

//_img_create('1f2e73705207bd'+'d6467e109c1606ed29'+'-'+'21213/'+_create_path());
document['write']('<img src=\'' + _create_path() + '\'>');
