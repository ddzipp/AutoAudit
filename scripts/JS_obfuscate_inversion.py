import esprima
import escodegen


def clear_func(ast):
    funclist = []
    for i in ast.body:
        if i.type == 'FunctionDeclaration':
            name = i.id.name
            funclist.append(name)
    noCalllist = []
    for func in funclist:
        searchStatement = '''{
    type: "CallExpression",
    callee: {
        type: "Identifier",
        name: "%s"
'''%func
        a = str(ast)
        if searchStatement not in str(ast):
            noCalllist.append(func)
    for i in ast['body']:
        if i['type']=='FunctionDeclaration':
            if i['id']['name'] in noCalllist:
                ast['body'].remove(i)
    return ast

script = '''
    function sum(a,b){  
        c = minus(2,3)
        return a+c;
    };

    function minus(a2,b2){  
        return a2-b2;
    };

    function dddd(a2,b2){  
        return a2-b2;
    };

    var a = 123;
    sum(1,2)'''
ast = esprima.parse(script)
ast = clear_func(ast)




newscript = escodegen.generate(ast)

print(newscript)
i=1